from fastapi import FastAPI
import uvicorn

from intelligence_task_manager.routes import agent_routes, mission_routes, report_routes

app = FastAPI()

app.include_router(agent_routes.router)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)