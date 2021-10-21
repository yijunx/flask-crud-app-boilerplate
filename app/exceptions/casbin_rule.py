class PolicyDoesNotExist(Exception):
    """raised when the policy is not found"""

    def __init__(self, item_id: str) -> None:
        self.message = f"Item {item_id} does not exist"
        self.status_code = 404
        super().__init__(self.message)


class PolicyIsAlreadyThere(Exception):
    """raised when the v0 and v1 duplicates"""

    def __init__(self, item_name: str) -> None:
        self.message = f"Item name {item_name} is already there"
        self.status_code = 409
        super().__init__(self.message)
