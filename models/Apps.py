from db_repository.BaseRepositories import BaseModelSchema
from db_repository.volunteer_repository import *
from db_repository.needy_repository import *
from db_repository.apartment_repository import *
from db_repository.schemas.apartment import *
from db_repository.schemas.needy import *
from db_repository.schemas.volunteer import *
from models.Volunteer import Volunteer
from models.Apartment import Apartment
from models.Needy import Needy
from threading import Lock

mutex = Lock()


class HousingApp:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_repositories()

    @property
    def volunteers(self) -> List[Volunteer]:
        return self.volunteer_repo.get_all()

    @property
    def apartaments(self) -> List[Apartment]:
        return self.apartment_repo.get_all()

    @property
    def needys(self) -> List[Needy]:
        return self.needy_repo.get_all()

    def _init_repositories(self):
        self.volunteer_repo = VolunteerRepository(mutex, self.db_path)
        self.needy_repo = NeedyRepository(mutex, self.db_path)
        self.apartment_repo = ApartmentRepository(mutex, self.db_path)

    def register_volunteer(self, name: str, contact: str) -> BaseModelSchema | None:
        volunteer = VolunteerSchema(name=name, contact=contact)
        volunteer_id = self.volunteer_repo.create(volunteer)
        return self.volunteer_repo.get(volunteer_id)

    def register_evacuee(self, name: str, contact: str, region: str, how_much_people: int) -> NeedySchema:
        evacuee = NeedySchema(
            name=name,
            contact=contact,
            region=region,
            how_much_peoples=how_much_people
        )
        evacuee_id = self.needy_repo.create(evacuee)
        return self.needy_repo.get(evacuee_id)

    def add_apartment(
            self,
            volunteer_name: str,
            location: str,
            rooms: int,
            has_mamad: bool,
            price: float,
            regions: str
    ) -> ApartmentSchema:
        if not self.volunteer_repo.get_by_name(volunteer_name):
            raise ValueError("Volunteer not found")

        apartment = ApartmentSchema(
            owner=volunteer_name,
            location=location,
            rooms=rooms,
            has_mamad=str(has_mamad),
            price=str(price),
            accepted_regions=regions,
            is_available=True
        )
        apartment_id = self.apartment_repo.create(apartment)

        # Связываем квартиру с волонтером
        self.volunteer_repo.add_apartment(volunteer_name, apartment_id)
        return self.apartment_repo.get(apartment_id)

    def search_apartments(self, evacuee_name: str) -> list[ApartmentSchema]:
        evacuee = self.needy_repo.get_by_name(evacuee_name)
        if not evacuee:
            raise ValueError("Evacuee not found")

        return self.apartment_repo.search_available(
            evacuee.region,
            1
        )

    def book_apartment(self, apartment_id: int, evacuee_name: str) -> bool:
        apartment = self.apartment_repo.get(apartment_id)
        evacuee = self.needy_repo.get_by_name(evacuee_name)

        if not apartment or not evacuee:
            return False

        # Проверяем условия бронирования
        if (
                apartment.is_available and
                (evacuee.region in apartment.accepted_regions or "all" in apartment.accepted_regions)
        ):
            updated_apartment = apartment.copy(update={"is_available": False})
            self.apartment_repo.update(apartment_id, updated_apartment)
            return True

        return False

    def get_volunteer_apartments(self, volunteer_id: int) -> list[ApartmentSchema]:
        apartment_ids = self.volunteer_repo.get_apartments(volunteer_id)
        return [self.apartment_repo.get(aid) for aid in apartment_ids]

    def list_available_apartments(self) -> list[ApartmentSchema]:
        return self.apartment_repo.get_all_available()

    def list_all_evacuees(self) -> list[NeedySchema]:
        return self.needy_repo.get_all()

    def list_all_volunteers(self) -> list[VolunteerSchema]:
        return self.volunteer_repo.get_all()
