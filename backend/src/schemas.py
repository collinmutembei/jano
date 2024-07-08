from pydantic import BaseModel
from datetime import datetime, UTC


class UserBase(BaseModel):
    username: str


class UserCredentials(UserBase):
    password: str


class User(UserBase):
    id: int


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JournalEntryBase(BaseModel):
    title: str
    content: str
    category: str
    date: datetime = datetime.now(UTC)


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryUpdate(JournalEntryBase):
    title: str = None
    content: str = None
    category: str = None
    date: datetime = None


class JournalEntry(JournalEntryBase):
    id: int
    user_id: int
