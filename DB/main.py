from gen_ai_hub.proxy.langchain import init_llm
from langchain_core.language_models import BaseLanguageModel
from DB.utils import  add_github_repo_to_db
from DB.vector_db import VectorDB
from scanners.github.github_scanner import GitHubScanner
from scanners.github.github_settings import GitHubSettings

from db_types import DBType
from settings import VectorDBSettings


if __name__ == '__main__':
    # init GitHubSettings for github_scanner
    token = "github_token"
    repo_name = "devx-wing/ucl-provider"
    base_url = "https://github.wdf.sap.corp/api/v3"
    user_name = "I583925"
    github_settings = GitHubSettings(user_name, token, repo_name, base_url)
    github_scanner = GitHubScanner(github_settings)

    # init VectorDB
    db_api_key = "db_api_key"
    db_url = "https://bac12217-a8c1-42c2-96a2-d60825ac7f4d.us-west-2-0.aws.cloud.qdrant.io:6333"
    settings = VectorDBSettings(db_type=DBType.QDRANT, url=db_url, api_key=db_api_key)
    vector_db = VectorDB(settings)

    # init LLM
    llm: BaseLanguageModel = init_llm('gpt-4o')

    # add github repo to vectorDB
    add_github_repo_to_db(github_scanner=github_scanner, vector_db=vector_db, llm=llm)
