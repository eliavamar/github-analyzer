from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient

from tools.github.GithubTools import GithubTools


class GithubAgent:
    def __init__(self, client: QdrantClient, collection_name: str, llm: BaseLanguageModel):
        self.client = client
        self.collection_name = collection_name
        self.llm = llm
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        github_tools = GithubTools(self.client, self.collection_name)
        tools = [github_tools.get_query_with_diff_tool()]
        system_message = (
            "You are an AI assistant that helps users troubleshoot and analyze GitHub. "
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools)

    def get_agent(self):
        return self.agent_executor
