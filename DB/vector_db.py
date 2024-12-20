from qdrant_client import QdrantClient
from DB.db_types import DBType
from DB.settings import VectorDBSettings


class VectorDB:
    """VectorDB class to initialize and return a vector database client based on the settings."""

    def __init__(self, settings: VectorDBSettings):
        self.settings = settings
        self.client = self._initialize_client()

    def _initialize_client(self):
        if self.settings.db_type.name == DBType.QDRANT.name:
            return self._initialize_qdrant_client()
        else:
            raise ValueError(f"Unsupported database type: {self.settings.db_type}")

    def _initialize_qdrant_client(self) -> QdrantClient:
        return QdrantClient(
            url=self.settings.url,
            api_key=self.settings.api_key
        )

    def get_client(self):
        """Returns the initialized vector database client."""
        return self.client

    def add(self, collection_name, documents, metadata):
        """Add documents with metadata to the collection."""

        self.client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata
        )



# Example usage
# if __name__ == "__main__":
#
#     # Example with URL
#     settings = VectorDBSettings(db_type=DBType.QDRANT, url="<URL>", api_key="<token>")
#     vector_db = VectorDB(settings)
#     client = vector_db.get_client()
#     # Define documents and metadata
#     docs = ["Qdrant has Langchain integrations", "Qdrant also has Llama Index integrations"]
#     metadata = [
#         {"source": "Langchain-docs", "case": "diff"},  # Add 'case' key with 'diff' value
#         {"source": "Linkedin-docs", "case": "other"},  # Example with a different 'case' value
#     ]
#     ids = [42, 2]
#
#     # Use the add method to insert documents with metadata
#     client.add(
#         collection_name="demo_collection",
#         documents=docs,
#         metadata=metadata,
#         ids=ids
#     )
#
#     # Define the filter for 'case' field with value 'diff'
#     filter_condition = Filter(
#         must=[FieldCondition(
#             key="case",
#             match=MatchValue(value="diff")
#         )]
#     )
#
#     # Perform the query with the filter
#     search_result = client.query(
#         collection_name="demo_collection",
#         query_text="This is a query document",
#         query_filter=filter_condition  # Apply the filter here
#     )
#
#     # Print the search result
#     print(search_result)


