from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional #B
from uuid import UUID, uuid4 #Garunees a unique id

app = FastAPI()

## Basic pydantic model to have correct validation
class Task(BaseModel):
    id: Optional[UUID] = None #Optional means you don't have to pass an id, UUID is type
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = [] ##Typically you would connect this to a real database

##=============================== CREATING A POST ROUTE ===========================##
@app.post("/tasks/", response_model=Task) #Defines that we use this pydantic model to encode json returned
def create_task(task: Task): #Specifies that we want to accept a new task using this pydantic model
    task.id = uuid4() #Gives us a new unique identifier
    tasks.append(task) #This would be switched out with code to append to the database
    return task


##=============================== CREATING A GET ROUTE ===========================##
@app.get("/tasks/", response_model = List[Task]) #Ok to have same endpoint as long as different request type, list[task] returns all tasks
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found") #RAISE HTTPException, FastAPI handles display

@app.put("/tasks/{task_id}", response_model = Task)
def update_task(task_id: UUID, task_update: Task):
    for id, task in enumerate(tasks):
        if task.id == task_id:
            ## When patching you only want to update the relevent keys. Exclude_unset ensures that you only
            ## update the specific keys that are changing
            updated_task = task.copy(update=task_update.dict(exclude_unset=True)) 
            tasks[id] = updated_task #Substitute for what normally is an update db command
            return updated_task

    raise HTTPException(status_code=404, detail="Task not found") #RAISE HTTPException, FastAPI handles display

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id:UUID):
    for id, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(id)

    raise HTTPException(status_code=404, detail="Task not found") #RAISE HTTPException, FastAPI handles display
           


## TEST NOTES
### CAN NOT USE 0.0.0.0:8000 to connect from browser, use http://localhost:8000/
### Fast API allows you to go to http://localhost:8000/docs for docs on the api usage


## You can only use await inside of functions created with async def
### Await keyword pauses the execution of a coroutine until awaitable object completes
### Instead of blocking entire program, it yields control back to the asyncio event loop
### Event loop performs other routines while waiting.

# async def read_results():
#     results = await some_library()
#     return results

##=============================== CREATING A GET ROUTE ===========================##


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_fastapi_tutorial:app", host="0.0.0.0", port=8000, reload=True)
 