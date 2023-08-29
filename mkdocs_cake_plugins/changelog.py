import re, os

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.utils.meta import get_data

from typing import Any, Dict

from git import Repo

from .utils.markdown_utils import get_title

class ChangelogPlugin(BasePlugin):
    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
    )

    enabled = True

    abbrs = {
        "高级语言程序设计": ["ALP"],
    }
    
    def on_config(self, config: config_options.Config, **kwargs) -> Dict[str, Any]:
        if not self.enabled:
            return config
        
        if not self.config.get("enabled"):
            return config

        self.repo = Repo(".")

    def on_page_markdown(
        self, markdown: str, page: Page, config: config_options.Config, files, **kwargs
    ) -> str:
        if not self.enabled:
            return markdown
        
        if not self.config.get("enabled"):
            return markdown

        if not page.meta.get("changelog"):
            return markdown
        
        changelogs = self._get_changelog_items(page)

        markdown = markdown.replace("{{ changelog }}", changelogs)

        return markdown
    
    def _get_changelog_items(self, page: Page):
        template = """- <span style="font-family: var(--md-code-font-family)">{time} [{commit_sha}]({commit_url}) </span>{commit_message}{links}"""
        res = ""
        year = 1970
        for commit in self.repo.iter_commits():
            now_year = commit.committed_datetime.year
            if now_year != year:
                year = now_year
                res += f"\n## {year} 年\n"
            commit_sha = commit.hexsha[:7]
            commit_url = f"https://github.com/shu-cake1salie/SHU-Cyberspace-Security-101/commit/{commit.hexsha}"
            message = commit.message.split("\n")[0]
            if message.startswith("Merge pull request"):
                continue
            commit_message = re.sub(r"#(\d+)", r"[#\1](https://github.com/shu-cake1salie/SHU-Cyberspace-Security-101/pull/\1)", message)
            time = commit.committed_datetime.strftime("%m-%d")

            changed_filenames = commit.stats.files.keys()
            docs_filenames = [
                filename for filename in changed_filenames 
                    if filename.startswith("docs/") and 
                       filename.endswith(".md") and 
                       filename.count("/") == 3 and
                       os.path.exists(filename)
            ]
            links = ""
            extra_count = 0
            for doc_path in docs_filenames:
                title = get_title(doc_path).strip()
                doc_url = doc_path.replace("docs/", "https://shu-cake1salie.github.io/SHU-Cyberspace-Security-101/").replace("index.md", "")
                search_strs = [title] + self.abbrs.get(title, [])
                _, meta = get_data(open(doc_path, "r", encoding="utf-8").read())
                if meta.get("abbrs"):
                    search_strs += meta.get("abbrs")
                for search_str in search_strs:
                    if search_str in commit_message:
                        commit_message = commit_message.replace(search_str, f"[{search_str}]({doc_url})")
                        break
                else:
                    if extra_count == 4:
                        links += "..."
                        extra_count += 1
                        continue
                    elif extra_count == 5:
                        continue
                    links += f"[{title}]({doc_url}) "
                    extra_count += 1

            if links:
                links = "\n    - 🔗 " + links
            
            res += template.format(commit_sha=commit_sha, commit_url=commit_url, commit_message=commit_message, links=links, time=time) + "\n"
        return res