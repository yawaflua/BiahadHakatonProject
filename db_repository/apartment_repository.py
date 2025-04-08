import array
from typing import Optional, List

from db_repository.BaseRepositories import BaseCRUDRepository
from db_repository.schemas.apartment import ApartmentSchema
import json


class ApartmentRepository(BaseCRUDRepository):
    table_name = "apartments"
    schema = ApartmentSchema

    def _get_columns_definition(self) -> str:
        base_columns = super()._get_columns_definition()
        # Добавляем кастомные поля, которые не обрабатываются автоматически
        return (
            "owner TEXT NOT NULL, "
            "location TEXT NOT NULL, "
            "rooms INTEGER NOT NULL, "
            "has_mamad TEXT NOT NULL, "
            "price TEXT NOT NULL, "
            "accepted_regions TEXT NOT NULL, "
            "is_available INTEGER NOT NULL"
        )

    def create(self, item: ApartmentSchema) -> int:
        item_dict = item.model_dump()
        return super().create(self.schema(**item_dict))

    def get(self, item_id: int) -> Optional[ApartmentSchema]:
        result = super().get(item_id)
        if result:
            result_dict = result.dict()
            result_dict["accepted_regions"] = result_dict["accepted_regions"]
            return ApartmentSchema(**result_dict)
        return None

    def search_available(
            self,
            region: str,
            min_rooms: int = 0,
    ) -> List[ApartmentSchema]:
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE is_available = 1 
          AND rooms >= ? 
        """
        params = (min_rooms,)

        results = self._execute(query, params, fetch=True)
        return [
            self._parse_result(row)
            for row in results
            if (region in row["accepted_regions"] or "all" in row["accepted_regions"])
        ]

    def _parse_result(self, row: tuple) -> ApartmentSchema:
        return ApartmentSchema(
            id=row["id"],
            owner=row["owner"],
            location=row["location"],
            rooms=row["rooms"],
            has_mamad=row["has_mamad"],
            price=row["price"],
            accepted_regions=row["accepted_regions"],
            is_available=bool(row["is_available"]),
        )
