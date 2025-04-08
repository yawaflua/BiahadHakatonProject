from typing import List

from db_repository.BaseRepositories import BaseCRUDRepository
from db_repository.schemas.needy import NeedySchema


class NeedyRepository(BaseCRUDRepository):
    table_name = "needies"
    schema = NeedySchema

    def _get_columns_definition(self) -> str:
        return (
            "name TEXT NOT NULL, "
            "contact TEXT NOT NULL, "
            "region TEXT NOT NULL, "
            "how_much_peoples INTEGER NOT NULL"
        )

    def get_by_region(self, region: str) -> List[NeedySchema]:
        query = f"SELECT * FROM {self.table_name} WHERE region = ?"
        results = self._execute(query, (region,), fetch=True)
        return [self.schema(**dict(row)) for row in results]
