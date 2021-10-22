class NotAuthorized(Exception):
    def __init__(self, resource_id: str, operation: str, user_id: str) -> None:
        self.status_code = 403
        self.message = "Not authorized"
        super().__init__(self.message)
