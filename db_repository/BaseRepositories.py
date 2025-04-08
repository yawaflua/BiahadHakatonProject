import sqlite3
from typing import Type, Optional, List
from pydantic import BaseModel
from threading import Lock


class BaseRepository:
    def __init__(self, mutex: Lock, db_path: str = "app.db"):
        self.mutex = mutex
        self.db_path = db_path
        self._init_db()

    @property
    def _connection(self) -> sqlite3.Connection:
        """Создает новое соединение для каждого запроса"""
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Инициализация таблиц в базе данных"""
        with self.mutex:
            with self._connection as conn:
                cursor = conn.cursor()
                statements = self.create_table_sql.split(';')
                for stmt in statements:
                    stmt = stmt.strip()
                    if stmt:
                        cursor.execute(stmt)
                conn.commit()

    @property
    def create_table_sql(self) -> str:
        """Должен быть переопределен в дочерних классах"""
        raise NotImplementedError

    def _execute(
            self,
            sql: str,
            params: tuple = (),
            fetch: bool = False
    ) -> Optional[List[dict]]:
        """Общий метод для выполнения запросов с возвратом словарей"""
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)

            if fetch:
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results

            conn.commit()
            return None


class BaseModelSchema(BaseModel):
    id: Optional[int] = None


class BaseCRUDRepository(BaseRepository):
    table_name: str = ""
    schema: Type[BaseModelSchema] = BaseModelSchema

    @property
    def create_table_sql(self) -> str:
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {self._get_columns_definition()}
        );
        """

    def _get_columns_definition(self) -> str:
        """Генерирует SQL-определение колонок на основе модели Pydantic"""
        fields = self.schema.model_fields
        columns = []
        for name, field in fields.items():
            if name == "id":
                continue
            sql_type = "TEXT" if field.annotation == str else "INTEGER"
            nullable = "NOT NULL" if not field.is_required else ""
            columns.append(f"{name} {sql_type} {nullable}")
        return ", ".join(columns)

    def create(self, item: BaseModelSchema) -> int:
        fields = item.dict(exclude={"id"})
        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))

        sql = f"""
        INSERT INTO {self.table_name} ({columns})
        VALUES ({placeholders})
        """
        self._execute(sql, tuple(fields.values()))
        return self._get_last_insert_id()

    def get(self, item_id: int) -> Optional[BaseModelSchema]:
        sql = f"SELECT * FROM {self.table_name} WHERE id = ?"
        result = self._execute(sql, (item_id,), fetch=True)
        return self.schema(**dict(result[0])) if result else None

    def get_by_name(self, item_id: str) -> Optional[BaseModelSchema]:
        sql = f"SELECT * FROM {self.table_name} WHERE name = ?"
        result = self._execute(sql, (item_id,), fetch=True)
        return self.schema(**dict(result[0])) if result else None

    def get_all(self) -> List[BaseModelSchema]:
        sql = f"SELECT * FROM {self.table_name}"
        results = self._execute(sql, fetch=True)
        return [self.schema(**dict(row)) for row in results]

    def update(self, item_id: int, item: BaseModelSchema) -> bool:
        fields = item.dict(exclude={"id"})
        set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])

        sql = f"""
        UPDATE {self.table_name}
        SET {set_clause}
        WHERE id = ?
        """
        params = (*fields.values(), item_id)
        self._execute(sql, params)
        return True

    def delete(self, item_id: int) -> bool:
        sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        self._execute(sql, (item_id,))
        return True

    def _get_last_insert_id(self) -> int:
        result = self._execute("SELECT last_insert_rowid()", fetch=True)
        return result[0]["last_insert_rowid()"] if result else 0
