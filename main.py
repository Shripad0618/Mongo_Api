from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

mongouri = os.getenv("mongouri")
Client = AsyncIOMotorClient(mongouri)
db = Client["euron"]
euron_data = db["euron_coll"]

app = FastAPI()

class EuronData(BaseModel):
    name: str
    city: str
    phone: int
    course: str




@app.post("/euron/insert")
async def euron_data_insert_helper(data:EuronData):
    result = await euron_data.insert_one(data.dict())
    return {"message": "Data inserted successfully", "id": str(result.inserted_id)}

@app.get("/euron/getdata")
async def get_euron_data():
    euron_data_list = []
    async for data in euron_data.find({}):
        data["_id"] = str(data["_id"])
        euron_data_list.append(data)
    return euron_data_list


@app.get("/euron/showdata/{name}")
async def get_euron_data_by_name(name: str):
    data = await euron_data.find_one({"name": name})
    if data:
        data["_id"] = str(data["_id"])
        return data
    else:
        raise HTTPException(status_code=404, detail="Data not found")

#@app.get("/euron/getdata/{id}")
#async def get_euron_data_by_id(id: str):