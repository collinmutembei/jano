from datetime import UTC, datetime

from pydantic import BaseModel


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
    title: str = None  # type: ignore[assignment]
    content: str = None  # type: ignore[assignment]
    category: str = None  # type: ignore[assignment]
    date: datetime = None  # type: ignore[assignment]


class JournalEntry(JournalEntryBase):
    id: int
    user_id: int
