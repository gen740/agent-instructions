"""All writes, Git repositories, and Codex state live in temporary fixtures."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/link-codex.sh"
CODEX = os.environ.get("CODEX_TEST_BINARY")


def skill(parent, name):
    directory = parent / name
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill {name}.\n---\n\nFixture.\n"
    )
    return directory


class AppServer:
    def __init__(self, env, cwd):
        self.log = tempfile.TemporaryFile(mode="w+")
        self.process = subprocess.Popen(
            [CODEX, "app-server", "--stdio"],
            cwd=cwd, env=env, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log,
        )
        self.messages = queue.Queue()
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()
        self.sequence = 0

    def read(self):
        try:
            for line in self.process.stdout:
                self.messages.put(json.loads(line))
        finally:
            self.messages.put(None)

    def request(self, method, params):
        self.sequence += 1
        self.send({"id": self.sequence, "method": method, "params": params})
        deadline = time.monotonic() + 30
        while True:
            try:
                message = self.messages.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty:
                self.log.seek(0)
                raise AssertionError(f"{method} timed out\n{self.log.read()[-4000:]}")
            if message is None:
                self.log.seek(0)
                raise AssertionError(f"App server exited\n{self.log.read()[-4000:]}")
            if message.get("id") == self.sequence:
                if "error" in message:
                    raise AssertionError(message["error"])
                return message["result"]

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        self.reader.join(timeout=5)
        self.process.stdin.close()
        self.process.stdout.close()
        self.log.close()


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-links-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "home"
        self.codex_home = self.home / ".codex"
        self.skills = self.home / ".agents/skills"
        self.repo = self.root / "repo with spaces"
        (self.repo / "scripts").mkdir(parents=True)
        self.home.mkdir()
        shutil.copy2(SCRIPT, self.repo / "scripts/link-codex.sh")
        (self.repo / "instructions.md").write_text("Fixture instructions.\n")
        skill(self.repo / "skills", "initial-skill")
        # Only the spawned processes get a fixture home; the user's home is untouched.
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex_home))

    def link(self, success=True):
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/link-codex.sh")],
            env=self.env, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def test_install_repeat_and_new_skill(self):
        self.link()
        self.assertEqual((self.codex_home / "AGENTS.md").read_text(), "Fixture instructions.\n")
        self.link()
        skill(self.repo / "skills", "added-skill")
        self.assertTrue((self.skills / "agent-instructions/added-skill/SKILL.md").is_file())

    def test_preserves_unrelated_and_legacy_skills(self):
        unrelated = skill(self.skills, "unrelated-skill")
        legacy = self.codex_home / "skills"
        legacy.mkdir(parents=True)
        (legacy / "initial-skill").symlink_to(self.repo / "skills/initial-skill")
        (legacy / "other-link").symlink_to(unrelated)
        config = self.codex_home / "config.toml"
        config.write_text("# existing config\n")
        self.link()
        self.link()
        self.assertEqual(config.read_text(), "# existing config\n")
        self.assertTrue((unrelated / "SKILL.md").is_file())
        self.assertEqual((legacy / "other-link").readlink(), unrelated)
        self.assertTrue((legacy / "initial-skill").is_symlink())

    def test_custom_codex_home_does_not_move_user_skill_root(self):
        self.codex_home = self.root / "custom codex"
        self.env["CODEX_HOME"] = str(self.codex_home)
        self.link()
        self.assertTrue((self.codex_home / "AGENTS.md").is_symlink())
        self.assertTrue((self.skills / "agent-instructions/initial-skill/SKILL.md").is_file())
        self.assertFalse((self.codex_home / "skills").exists())

    def test_conflicts_leave_existing_paths_untouched(self):
        for location in (self.skills / "agent-instructions", self.codex_home / "AGENTS.md"):
            for kind in ("file", "directory", "symlink", "dangling symlink"):
                with self.subTest(location=location, kind=kind):
                    location.parent.mkdir(parents=True, exist_ok=True)
                    target = self.root / "unrelated"
                    target.write_text("preserve me\n")
                    if kind == "file":
                        location.write_text("preserve me\n")
                    elif kind == "directory":
                        location.mkdir()
                        (location / "keep").write_text("preserve me\n")
                    else:
                        location.symlink_to(target if kind == "symlink" else self.root / "missing")
                    result = self.link(success=False)
                    self.assertIn("conflict:", result.stderr)
                    self.assertEqual(target.read_text(), "preserve me\n")
                    if kind == "directory":
                        self.assertEqual((location / "keep").read_text(), "preserve me\n")
                        shutil.rmtree(location)
                    elif "symlink" in kind:
                        self.assertTrue(location.is_symlink())
                        self.assertEqual(location.readlink(), target if kind == "symlink" else self.root / "missing")
                        location.unlink()
                    else:
                        self.assertEqual(location.read_text(), "preserve me\n")
                        location.unlink()
                    # Preflight must not partially install the other destination.
                    other = self.codex_home / "AGENTS.md" if location.parent == self.skills else self.skills / "agent-instructions"
                    self.assertFalse(other.exists() or other.is_symlink())

    @unittest.skipUnless(CODEX, "Set CODEX_TEST_BINARY to test actual Codex discovery")
    def test_codex_discovers_new_skill_after_git_pull(self):
        def git(cwd, *args):
            return subprocess.run(
                ["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True,
                env=dict(self.env, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull),
            )

        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Test Fixture")
        git(self.repo, "config", "commit.gpgsign", "false")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "Initial fixture")
        upstream = self.repo
        self.repo = self.root / "installed clone"
        git(self.root, "clone", str(upstream), str(self.repo))
        unrelated = skill(self.skills, "unrelated-skill")
        legacy = self.codex_home / "skills"
        legacy.mkdir(parents=True)
        (legacy / "initial-skill").symlink_to(self.repo / "skills/initial-skill")
        self.link()
        self.link()
        cwd = self.root / "unrelated project"
        cwd.mkdir()
        server = AppServer(self.env, cwd)
        self.addCleanup(server.close)
        server.request("initialize", {"clientInfo": {"name": "link-tests", "version": "1"}, "capabilities": {"experimentalApi": True}})
        server.send({"method": "initialized"})

        def discovered():
            result = server.request("skills/list", {"cwds": [str(cwd)], "forceReload": True})
            entry, = result["data"]
            self.assertEqual(entry["errors"], [])
            return [item for item in entry["skills"] if item["scope"] == "user"]

        before = discovered()
        self.assertEqual(sorted(item["name"] for item in before), ["initial-skill", "unrelated-skill"])
        self.assertTrue(all(item["enabled"] for item in before))
        skill(upstream / "skills", "added-after-pull")
        git(upstream, "add", ".")
        git(upstream, "commit", "-m", "Add a skill")
        git(self.repo, "pull", "--ff-only")
        # No linker invocation after pull, and the same app-server process re-scans.
        after = discovered()
        self.assertEqual(sorted(item["name"] for item in after), ["added-after-pull", "initial-skill", "unrelated-skill"])
        self.assertTrue(all(item["enabled"] for item in after))
        self.assertTrue((unrelated / "SKILL.md").is_file())
        self.assertTrue((legacy / "initial-skill").is_symlink())


if __name__ == "__main__":
    unittest.main()
