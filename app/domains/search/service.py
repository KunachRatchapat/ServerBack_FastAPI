from sqlmodel import Session

from app.domains.search.repository import SearchRepository
from app.domains.search.schemas import SearchResultItem


class SearchService:
    def __init__(self) -> None:
        self.repo = SearchRepository()

    def search(self, db: Session, keyword: str) -> list[SearchResultItem]:
        fruits = self.repo.search_fruits(db, keyword)
        vegs = self.repo.search_vegetables(db, keyword)
        results = [SearchResultItem(name=f.name) for f in fruits]
        results += [SearchResultItem(name=v.name) for v in vegs]
        return results
