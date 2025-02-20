class ManagerException(Exception):
    def __init__(
            self,
            code: int = 500,
            message: str = None,
    ) -> None:
        self.code = code
        self.message = message
