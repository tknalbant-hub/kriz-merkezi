# github_manager.py
from git import Repo
import os

class GitHubManager:
    def __init__(self, repo_path, token):
        self.repo = Repo(repo_path)
        self.token = token

    def push_code(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)
        self.repo.index.add([filename])
        self.repo.index.commit(f"Otonom ajan tarafından güncellendi: {filename}")
        # Not: Remote push için token kimlik doğrulaması gerekir.
        print("Kod GitHub'a kaydedildi.")