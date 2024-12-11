from gen_ai_hub.proxy.langchain import init_llm

from DB.db_types import DBType
from DB.settings import VectorDBSettings
from DB.vector_db import VectorDB
from agents.github.GithubAgent import GithubAgent
from tools.github.GithubTools import GithubTools

settings = VectorDBSettings(db_type=DBType.QDRANT,
                            url="https://bac12217-a8c1-42c2-96a2-d60825ac7f4d.us-west-2-0.aws.cloud.qdrant.io:6333",
                            api_key="p6ErOJYvqi-daabdLArES-QeBxAxfGYzE46i40ML1hx-5unp7DUFUA")
vector_db = VectorDB(settings)
client = vector_db.get_client()
collection_name = "https___github_wdf_sap_corp_api_v3_devx-wing_ucl-provider"


if __name__ == '__main__':
    qdrant_tools = GithubTools(client, collection_name)
    llm = init_llm('gpt-4o')
    agent_executor = GithubAgent(client, collection_name, llm).get_agent()
    result = agent_executor.invoke(
        {"input": "I have bug in the unit testing in uclTest.file, Do you know what the problem can be?"})
    print(result)
