from pydantic import BaseModel


class Settings(BaseModel):
    bot_api_key: str
    log_chat_id: str


class Config(BaseModel):
    stash: list[str]
    settings: Settings
