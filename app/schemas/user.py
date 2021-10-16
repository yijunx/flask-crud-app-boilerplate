from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str  # maybe only first name from google id token
    email: str
