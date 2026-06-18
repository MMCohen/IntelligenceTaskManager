from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from intelligence_task_manager.database.mission_db import MissionDB

mission_db = MissionDB()

router = APIRouter()

class NewMission(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int
    status: Literal["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"]



@router.post("/missions")
def add_new_mission(data: NewMission):
    if data.difficulty > 10 or data.difficulty < 1:
        msg = "difficulty must be btw 1-10"
        raise HTTPException(status_code=400, detail=msg)

    if data.importance > 10 or data.importance < 1:
        msg = "importance must be btw 1-10"
        raise HTTPException(status_code=400, detail=msg)

    mission_dict = data.model_dump()
    new_mission = mission_db.create_mission(mission_dict)

    return new_mission



@router.get("/missions")
def get_all_missions():
    all_missions = mission_db.get_all_missions()
    return all_missions


@router.get("/missions/{id}")
def get_mission_by_id(id: int):
    mission_data = mission_db.get_mission_by_id(id)

    if not mission_data:
        #todo: add message
        raise HTTPException(status_code=404)

    return mission_data


@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission_by_id(id: int, agent_id: int):

    is_mission_exist = mission_db.get_mission_by_id(id)
    is_agent_exist = mission_db.get_agent_by_id(agent_id)

    if not is_mission_exist:
        #todo: add message
        raise HTTPException(status_code=404, detail="mission dosnt exist")

    if not is_agent_exist:
        #todo: add message
        raise HTTPException(status_code=404, detail="agent dosnt exist")

    is_mission_in_status_new = is_mission_exist["status"].lower() == "new"
    is_agent_active = is_agent_exist["is_active"] == True

    if not is_mission_in_status_new:
        raise HTTPException(status_code=400, detail="Mission not available")

    if not is_agent_active:
        raise HTTPException(status_code=400, detail="Agent is not active")

    agent_count_open_missions = len(mission_db.get_open_missions_by_agent(agent_id))
    is_agent_allow_to_get_missions = agent_count_open_missions < mission_db.MAX_OPEN_MISSIONS_PER_AGENT

    if not is_agent_allow_to_get_missions:
        raise HTTPException(status_code=400, detail="Agent has 3 open missions")

    if is_mission_exist["risk_level"].lower() == "critical" and is_agent_exist["agent_rank"].lower() != "commander":
        raise HTTPException(status_code=400, detail="agent must be a commander in order to assigned critical missions")

    else:
        is_assign = mission_db.assign_mission(id, agent_id)
        return is_assign


@router.put("/missions/{id}/start")
def start_mission(id: int):
    is_mission_exist = mission_db.get_mission_by_id(id)

    if not is_mission_exist:
        # todo: add message
        raise HTTPException(status_code=404, detail="mission dosnt exist")

    mission_status:str = is_mission_exist["status"]
    if mission_status.upper() != "ASSIGNED":
        raise HTTPException(status_code=400)

    is_start = mission_db.update_mission_status(id, "IN_PROGRESS")
    return is_start


@router.put("/missions/{id}/complete")
def complete_mission(id: int):
    is_mission_exist = mission_db.get_mission_by_id(id)

    if not is_mission_exist:
        # todo: add message
        raise HTTPException(status_code=404, detail="mission dosnt exist")


    mission_status:str = is_mission_exist["status"]
    if mission_status.upper() != "IN_PROGRESS":
        raise HTTPException(status_code=400)

    is_start = mission_db.update_mission_status(id, "COMPLETED")
    #need to add complte to agent

    return is_start




@router.put("/missions/{id}/fail")
def fail_mission(id: int):
    is_mission_exist = mission_db.get_mission_by_id(id)

    if not is_mission_exist:
        # todo: add message
        raise HTTPException(status_code=404, detail="mission dosnt exist")

    mission_status: str = is_mission_exist["status"]
    if mission_status.upper() != "IN_PROGRESS":
        raise HTTPException(status_code=400)

    is_start = mission_db.update_mission_status(id, "FAILED")
    #need to add fail to agent

    return is_start


@router.put("/missions/{id}/cancel")
def cancel_mission(id: int):
    is_mission_exist = mission_db.get_mission_by_id(id)

    if not is_mission_exist:
        # todo: add message
        raise HTTPException(status_code=404, detail="mission dosnt exist")

    mission_status: str = is_mission_exist["status"]
    if mission_status.upper() not in ("NEW", "ASSIGNED"):
        raise HTTPException(status_code=400)

    is_start = mission_db.update_mission_status(id, "CANCELLED")
    # need to add fail to agent

    return is_start

