
from fastapi import Body, Query, APIRouter

from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]
#hotels[per_page*(page-1):per_page*(page-1)+per_page]


@router.get("", summary="Вывод данных о выбранных отелях")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, ge=1, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),

):
    global hotels
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if id or title:
        return hotels_

    if pagination.page and pagination.per_page:
        return hotels[pagination.per_page*(pagination.page-1):pagination.per_page*(pagination.page-1)+pagination.per_page]
    return hotels_

@router.post("", summary="Создание данных о новом отеле")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Классный отель сочи",
        "name": "classniy_otel_sochi",
    }},
    "2": {"summary": "Отель дубай", "value": {
        "title": "дубай отель 5 звезд",
        "name": "dubai_hotel_5",
    }},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

@router.put("/{hotel_id}", summary="Изменение всех данных об отеле")
def change_all_params(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id-1]["title"] = hotel_data.title
    hotels[hotel_id-1]["name"] = hotel_data.name
    return {"status": "ok"}

@router.patch("/{hotel_id}", summary="Изменение выбранных данных об отеле")
def change_need_params(hotel_id: int, hotel_data: HotelPATCH = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "name": "luchiy_hotel",
    }},
})):
    global hotels
    if hotel_data.title:
        hotels[hotel_id-1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id-1]["name"] = hotel_data.name
    return {"status": "ok"}

@router.delete("/{hotel_id}", summary="Удаление данных об отеле")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}