from pydantic import BaseModel


class UserBase(BaseModel):
    usernmame: str
    email: str
    password: str


class UserDisplay(BaseModel):
    usernmame: str
    email: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    id: int
    username: str
    email: str
