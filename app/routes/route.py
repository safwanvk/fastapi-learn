from fastapi import APIRouter
from models.todos import Todo
from config.database import collection_name
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_todos():
      todos = collection_name.find()
      return list_serial(todos)

@router.post("/")
async def create_todo(todo: Todo):
    todo_dict = todo.dict()
    result = collection_name.insert_one(todo_dict)
    todo_dict["_id"] = str(result.inserted_id)
    return individual_serial(todo_dict)

@router.get("/{id}")
async def get_todo(id: str):
      todo = collection_name.find_one({"_id": ObjectId(id)})
      if todo:
            return individual_serial(todo)
      return {"error": "Todo not found"}, 404

@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
      todo_dict = todo.dict()
      result = collection_name.update_one({"_id": ObjectId(id)}, {"$set": todo_dict})

      if result.matched_count == 0:
            return {"error": "Todo not found"}

      todo_dict["_id"] = id
      return individual_serial(todo_dict)

@router.delete("/{id}")
async def delete_todo(id: str):
      result = collection_name.delete_one({"_id": ObjectId(id)})

      if result.deleted_count == 0:
            return {"error": "Todo not found"}

      return {"message": "Todo deleted successfully"}