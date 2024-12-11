class FileChangeInfo:
    """
    Concrete implementation of FileChangeInfo.
    """

    def __init__(self, file_path: str, change_type: str, change_content: str):
        self._file_path = file_path
        self._change_type = change_type
        self._change_content = change_content

    def get_file_path(self) -> str:
        return self._file_path

    def get_change_type(self) -> str:
        return self._change_type

    def get_change_content(self) -> str:
        return self._change_content
