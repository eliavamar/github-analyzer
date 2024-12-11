from gen_ai_hub.proxy.langchain import init_llm

from DB.db_types import DBType
from DB.settings import VectorDBSettings
from DB.vector_db import VectorDB
from graphAgents.GithubTools import GithubTools
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from langchain_core.prompts import ChatPromptTemplate

settings = VectorDBSettings(db_type=DBType.QDRANT,
                            url="<url>",
                            api_key="<token>")
vector_db = VectorDB(settings)
client = vector_db.get_client()
collection_name = "https___github_wdf_sap_corp_api_v3_devx-wing_ucl-provider"


if __name__ == '__main__':
    qdrant_tools = GithubTools(client, collection_name)
    llm = init_llm('gpt-4o')
    tools = [qdrant_tools.get_query_with_diff_tool()]
    system_message = (
        "You are an AI assistant that helps users troubleshoot GitHub issues. "
        "If there is a problem in the code, use the `query_with_diff` tool to analyze changes between the two latest "
        "tags. "
        "If the issue does not seem related to recent code changes, inform the user that no relevant issues could be "
        "identified. "
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    result = agent_executor.invoke(
        {"input": "I have bug in the unit testing in uclTest.file, Do you know what the problem can be?"})
    print(result)
