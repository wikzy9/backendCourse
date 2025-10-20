from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

    return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })

@app.put("/hotels/{hotel_id}")
def change_all_params(
    hotel_id: int = Body(embed=True),
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    hotels[hotel_id-1]["title"] = title
    hotels[hotel_id-1]["name"] = name
    return {"status": "ok"}

@app.patch("/hotels/{hotel_id}")
def change_need_params(
    hotel_id: int = Body(embed=True),
    title: str | None = Body(None, embed=True),
    name: str | None = Body(None, embed=True),
):
    global hotels
    if title:
        hotels[hotel_id-1]["title"] = title
    if name:
        hotels[hotel_id-1]["name"] = name
    return {"status": "ok"}

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True)