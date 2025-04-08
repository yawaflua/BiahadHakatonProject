from typing import Optional

from pydantic import BaseModel

from db_repository.BaseRepositories import BaseCRUDRepository
from models.Volunteer import Volunteer


class VolunteerCreate(BaseModel, Volunteer):
    id: int


class VolunteerSchema(VolunteerCreate):
    id: int = None
