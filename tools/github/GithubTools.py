from qdrant_client import QdrantClient
from qdrant_client.http.models import MatchValue
from qdrant_client.models import Filter, FieldCondition
from langchain.tools import tool


class GithubTools:
    """
    A class to interact with the Qdrant vector database using predefined query tools.
    """

    def __init__(self, client: QdrantClient, collection_name: str):
        """
        Initializes the QdrantQueryTool with a client and collection name.

        Args:
            client (QdrantClient): The initialized Qdrant client.
            collection_name (str): The name of the Qdrant collection.
        """
        self.client = client
        self.collection_name = collection_name

    def _query_vector_db(self, case_value: str, query_text: str, limit: int = 10):
        """
        Internal method to query the Qdrant vector database with a given 'case' filter.

        Args:
            case_value (str): The value to filter by in the 'case' field.
            query_text (str): The query text to use for the search.
            limit (int, optional): The maximum number of results to return. Defaults to 10.

        Returns:
            list: A list of search results.
        """
        # Build the filter condition for the 'case' field
        filter_condition = Filter(
            must=[
                FieldCondition(
                    key="case",
                    match=MatchValue(value=case_value)
                )
            ]
        )

        # Perform the query
        search_result = self.client.query(
            collection_name=self.collection_name,
            query_text=query_text,
            query_filter=filter_condition,
            limit=limit
        )

        return search_result

    def get_query_with_diff_tool(self):
        @tool
        def query_with_diff(query_text: str, limit: int = 10):
            """
            Retrieves the differences between the two most recent versions of a GitHub repository,
            based on a given query. The repository name corresponds to the 'collection_name' already available.

            Args:
                query_text (str): The query to search for related documentation.
                limit (int): The number of most relevant code documentation entries to return (default is 10).

            Returns:
                list: A list of code documentation entries related to the query and the differences between
                      the latest versions of the repository.
            """
            return self._query_vector_db(case_value="diff", query_text=query_text, limit=limit)

        return query_with_diff

    def get_query_with_original_tool(self):
        @tool
        def query_with_original(query_text: str, limit: int = 10):
            """
            Queries the Qdrant vector database with 'case' set to 'original' and retrieves
            the latest release version of a given GitHub repository.

            This tool can be used to get information about the most recent release (version)
            of a GitHub repository, providing insights into the latest stable version of the code.

            Args:
                query_text (str): The query text to use for the search.
                limit (int, optional): The maximum number of results to return. Defaults to 10.
            """
            return self._query_vector_db(case_value="original", query_text=query_text, limit=limit)

        return query_with_original
