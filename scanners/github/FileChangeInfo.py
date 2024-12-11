from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser


class FileChangeInfo:
    """
    Concrete implementation of FileChangeInfo.
    """

    def __init__(self, file_path: str, change_type: str, change_content: str):
        self._file_path = file_path
        self._change_type = change_type
        self._change_content = change_content
        self._summary = None

    def __str__(self):
        return f"FileChangeInfo(file_path={self._file_path}, change_type={self._change_type}, change_content={self._change_content})"

    def get_file_path(self) -> str:
        return self._file_path

    def get_change_type(self) -> str:
        return self._change_type

    def get_change_content(self) -> str:
        return self._change_content

    def get_summary(self, llm: BaseLanguageModel) -> str:
        if self._summary is not None:
            return self._summary
        template = """You are an expert software engineer. You are given a file change from a GitHub repository. Your task is to summarize the changes in exactly three sentences.

                        File path: {file_path}
                        Change type: {change_type}
                        Change content (GitHub diff format):
                        {change_content}

                        {question}"""

        prompt = PromptTemplate(template=template, input_variables=['question'])
        question = "Please summarize the changes made to this file in exactly three sentences."

        chain = prompt | llm | StrOutputParser()
        self._summary = chain.invoke({
            "question": question,
            "file_path": self._file_path,
            "change_type": self._change_type,
            "change_content": self._change_content
        })
        return self._summary
