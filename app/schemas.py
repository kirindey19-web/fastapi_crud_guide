from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)