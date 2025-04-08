from db_repository.BaseRepositories import BaseCRUDRepository
from db_repository.schemas.volunteer import VolunteerSchema
from typing import List


class VolunteerRepository(BaseCRUDRepository):
    table_name = "volunteers"
    schema = VolunteerSchema

    def _get_columns_definition(self) -> str:
        return (
            "name TEXT NOT NULL, "
            "contact TEXT NOT NULL"
        )

    @property
    def create_table_sql(self) -> str:
        return f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {self._get_columns_definition()}
            );

            CREATE TABLE IF NOT EXISTS volunteer_apartments (
                volunteer_id INTEGER NOT NULL,
                apartment_id INTEGER NOT NULL,
                FOREIGN KEY(volunteer_id) REFERENCES volunteers(id),
                FOREIGN KEY(apartment_id) REFERENCES apartments(id)
            );
            """

    def add_apartment(self, volunteer_id: int, apartment_id: int):
        query = """
        INSERT INTO volunteer_apartments (volunteer_id, apartment_id)
        VALUES (?, ?)
        """
        self._execute(query, (volunteer_id, apartment_id))

    def get_apartments(self, volunteer_id: int) -> List[int]:
        query = """
        SELECT apartment_id FROM volunteer_apartments
        WHERE volunteer_id = ?
        """
        results = self._execute(query, (volunteer_id,), fetch=True)
        return [row[0] for row in results] if results else []
