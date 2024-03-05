from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# sample requests and queries
@app.get("/")
async def root() :
    return {"message" : "Hello World"}

# sample path paramters => entries in URL
@app.get("/hello/{name}")
async def say_hello(name: str) :
    return {"message" : f"Hello {name}"}

# Path parameters predefined values
# https://fastapi.tiangolo.com/tutorial/path-params/
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/v1/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# query parametres are added as elements to the url e.g. items?skip=10&limit=3
# https://fastapi.tiangolo.com/tutorial/query-params/
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/v2/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Optional parameters added to query, one of the element in Union
from typing import Union

#In this case, there are 3 query parameters:
# needy, a required str.
# skip, an int with a default value of 0.
# limit, an optional int.

@app.get("/v3/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# if you want to send it as a request body you have to define the class inheritet from pydantic base model
# Request Body
# https://fastapi.tiangolo.com/tutorial/body/
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
# create model
@app.post("/v4/items/")
async def create_item(item: Item):
    return item
# using model

@app.post("/v5/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# all together

@app.put("/v6/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# If the parameter is also declared in the path, it will be used as a path parameter.
# If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
# If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

# additional status code:
# https://fastapi.tiangolo.com/advanced/additional-status-codes/

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.put("/v7/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Union[str, None] = Body(default=None),
    size: Union[int, None] = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


# Laboratory assignment
from copy import deepcopy

poll_id = 0
vote_id = 0
polls   = []

def get_poll_by_id(id: int):
    polls_with_certain_id = list(filter(lambda poll: poll["id"] == id, polls))
    if len(polls_with_certain_id) == 0:
        return None
    return polls_with_certain_id[0]

def get_vote_by_id(id: int, poll):
    votes_with_certain_id = list(filter(lambda vote: vote["id"] == id, poll["votes"]))
    if len(votes_with_certain_id) == 0:
        return None
    return votes_with_certain_id[0]

def poll_without_votes(poll):
    poll_copy = deepcopy(poll)
    del poll_copy["votes"]
    return poll_copy

@app.get("/v1/poll")
async def get_all_polls():
    return polls

@app.get("/v1/poll/{poll_id}")
async def get_poll(
    poll_id: int
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")
    return poll

@app.get("/v1/poll/{poll_id}/vote")
async def get_all_votes(
    poll_id: int
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")
    return poll["votes"]

@app.get("/v1/poll/{poll_id}/vote/{vote_id}")
async def get_vote(
    poll_id: int,
    vote_id: int
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")

    vote = get_vote_by_id(vote_id, poll)
    if vote is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Vote {vote_id} of poll {poll_id} not found")

    return vote

@app.post("/v1/poll")
async def create_poll(
    fields: list[str]
):
    global poll_id
    poll_id += 1
    poll = {
        "id":     poll_id,
        "fields": fields,
        "votes":  [],
    }
    polls.append(poll)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=poll)

@app.post("/v1/poll/{poll_id}/vote")
async def vote(
    poll_id: int,
    vote:    dict[str, str | int | float | bool]
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")

    if list(vote.keys()) != poll["fields"]:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=f"Invalid vote fields")

    global vote_id
    vote_id   += 1
    vote["id"] = vote_id
    poll["votes"].append(vote)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=vote)

@app.put("/v1/poll/{poll_id}")
async def edit_poll(
    poll_id: int,
    fields:  list[str]
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")

    if poll["fields"] != fields:
        poll["fields"] = fields
        poll["votes"].clear()

    return poll_without_votes(poll)

@app.put("/v1/poll/{poll_id}/vote/{vote_id}")
async def edit_vote(
    poll_id:  int,
    vote_id:  int,
    new_vote: dict[str, str | int | float | bool]
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")

    vote = get_vote_by_id(vote_id, poll)
    if vote is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Vote {vote_id} of poll {poll_id} not found")

    if list(new_vote.keys()) != poll["fields"]:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=f"Invalid vote fields")

    for field in new_vote:
        vote[field] = new_vote[field]

    return vote

@app.delete("/v1/poll/{poll_id}")
async def delete_poll(
    poll_id: int
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")
    polls.remove(poll)
    return poll

@app.delete("/v1/poll/{poll_id}/vote/{vote_id}")
async def delete_poll(
    poll_id: int,
    vote_id: int
):
    poll = get_poll_by_id(poll_id)
    if poll is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Poll {poll_id} not found")

    vote = get_vote_by_id(vote_id, poll)
    if vote is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Vote {vote_id} of poll {poll_id} not found")

    poll["votes"].remove(vote)
    return vote
