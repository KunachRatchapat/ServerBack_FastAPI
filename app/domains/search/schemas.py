from pydantic import BaseModel


class SearchResultItem(BaseModel):
    name: str
