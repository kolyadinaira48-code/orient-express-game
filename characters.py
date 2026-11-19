"""Персонажи игры (по Game Design Document, раздел 3)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Passenger:
    name_ru: str
    name_en: str
    age: int
    profession: str
    compartment: int
    ticket: str       # билет формата OE-XX-000
    case_id: str      # номер пассажирского дела CASE-0000
    status: str = "пассажир"

    @property
    def baggage_tag(self):
        """Багажная бирка BAG-XX-000 строится по билету: OE-AR-104 -> BAG-AR-104."""
        return "BAG-" + self.ticket[3:]


PASSENGERS = [
    Passenger("Адриан Рид", "Adrian Reed", 56, "предприниматель", 7,
              "OE-AR-104", "CASE-1042", "жертва"),
    Passenger("Клара Лоран", "Clara Laurent", 31, "журналистка", 3,
              "OE-CL-208", "CASE-2081"),
    Passenger("Эмиль Новак", "Emil Novak", 42, "бывший бухгалтер", 5,
              "OE-EN-317", "CASE-3175"),
    Passenger("Джулиан Мерсер", "Julian Mercer", 48, "юридический консультант", 9,
              "OE-JM-421", "CASE-4217", "убийца"),
    Passenger("Изабель Моро", "Isabelle Moreau", 39, "владелица художественной галереи", 2,
              "OE-IM-509", "CASE-5092"),
    Passenger("Томас Хейл", "Thomas Hale", 51, "железнодорожный инспектор", 4,
              "OE-TH-613", "CASE-6134"),
    Passenger("Елена Соколова", "Elena Sokolov", 28, "музыкант", 6,
              "OE-ES-722", "CASE-7226"),
    Passenger("Мартин Белл", "Martin Bell", 55, "предприниматель", 8,
              "OE-MB-835", "CASE-8358"),
]

STAFF = {
    "Анри Дюбуа": "старший проводник, обнаружил Рида в 23:05",
    "Отто Вайс": "сотрудник багажного отделения",
}
