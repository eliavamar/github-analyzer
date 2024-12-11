import re

from langchain_core.language_models import BaseLanguageModel

from DB.vector_db import VectorDB
from scanners.github.github_scanner import GitHubScanner


def sanitize_collection_name(name):
    # Remove invalid characters and replace spaces with underscores
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def add_github_repo_to_db(github_scanner: GitHubScanner, vector_db: VectorDB, llm: BaseLanguageModel):
    files_changes = github_scanner.get_latest_tags_diff(branch=github_scanner.github_settings.branch)

    docs, metadata = [], []
    for file_change in files_changes:
        docs.append(file_change.get_summary(llm))
        metadata.append({"source": file_change.get_change_content(), "case": "diff"})

    collection_name = sanitize_collection_name(f"{github_scanner.github_settings.base_url}_{github_scanner.github_settings.repo_name}")
    vector_db.add(collection_name, docs, metadata)