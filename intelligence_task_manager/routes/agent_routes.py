from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from intelligence_task_manager.database.agent_db import AgentDB

agent_db = AgentDB()


router = APIRouter()

class Agent(BaseModel):
    name: str
    specialty: str
    agent_rank: str


class UpdateAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: Literal["Junior", "Senior", "Commander"]


@router.post("/agents")
def add_new_agent(data: Agent):
    if not data.agent_rank in ("Junior", "Senior", "Commander"):
        msg = "not legit rank"
        raise HTTPException(status_code=400, detail=msg)

    if not data.name or not data.agent_rank or not data.specialty:
        msg = "must enter name, agent_rank and specialty"
        raise HTTPException(status_code=422, detail=msg)

    agent_dict = data.model_dump()
    new_agent = agent_db.create_agent(agent_dict)
    if new_agent:
        raise HTTPException(status_code=201, detail=new_agent)



@router.get("/agents")
def get_All_agents():
    agents = agent_db.get_all_agents()
    return agents


@router.get("/agents/{id}")
def get_agent_by_id(id: int):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        message = "agent does not exist"
        raise HTTPException(status_code=404, detail=message)

    return agent

@router.put("/agents/{id}")
def update_agent_by_id(id: int, data: UpdateAgent):
    is_agent_exist = agent_db.get_agent_by_id(id)

    if not is_agent_exist:
        message = "agent does not exist"
        raise HTTPException(status_code=404, detail=message)

    agent_dict = data.model_dump()
    is_update = agent_db.update_agent(id, agent_dict)

    if not is_update:
        message = {"message": f"agent id {id} could not be updated"}
        raise HTTPException(status_code=400, detail=message)

    return {"message": f"agent id {id} update successfully"}




@router.put("/agents/{id}/deactivate")
def deactivate_agent_by_id(id: int):
    is_agent_exist = agent_db.get_agent_by_id(id)

    if not is_agent_exist:
        message = "agent does not exist"
        raise HTTPException(status_code=404, detail=message)

    is_deleted = agent_db.deactivate_agent(id)
    if is_deleted:
        return "is_active=False"

    raise HTTPException(status_code=400, detail="somthing went wrong")



@router.get("/agents/{id}/performance")
def get_agent_performance(id: int):
    is_agent_exist = agent_db.get_agent_by_id(id)

    if not is_agent_exist:
        message = "agent does not exist"
        raise HTTPException(status_code=404, detail=message)

    agent_performance = agent_db.get_agent_performance(id)

    return agent_performance


