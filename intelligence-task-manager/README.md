

# Intelligence Task Manager

---

## System description:

The Intelligence Task Manager system is here to organizes missions and agents into a fix system that  

---

## Directory structure:

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```
---

## Tables structure:

#### Agents table:

| field_name         | type        | constraints                           | description                              |
|--------------------|-------------|---------------------------------------|------------------------------------------|
| id                 | INT         | AUTO_INCREMENT PRIMARY KEY            | the agent id                             |
| name               | VARCHAR(50) | NOT NULL                              | the agent name                           |
| specialty          | VARCHAR(50) | NOT NULL                              | what the agent specializes in            |
| is_active          | BOOLEAN	    | DEFAULT TRUE                          | is the agent active. False if not        |
| completed_missions | INT         | DEFAULT 0                             | how many missions completed by the agent |
| failed_missions    | INT         | DEFAULT 0                             | how many missions failed by the agent    |
| agent_rank         | ENUM        | NOT NULL ENUM Junior/Senior/Commander | the agent rank                           |


#### Missions table:

| field_name        | type         | constraints                                                                | description                                                                                     |
|-------------------|--------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| id                | INT          | AUTO_INCREMENT PRIMARY KEY                                                 | the mission unique id                                                                           |
| title             | VARCHAR(255) | NOT NULL                                                                   | the mission title                                                                               |
| description       | LONGTEXT     | NOT NULL                                                                   | the mission description. can be long text.                                                      |
| location          | VARCHAR(255) | NOT NULL                                                                   | the mission location. location by text, not coordinates.                                        |
| difficulty        | INT          | CHECK (0 > difficulty > 11)                                                | the mission difficulty by number. can be only between 1-10                                      |
| importance        | INT          | CHECK (0 > difficulty > 11)                                                | the mission importance by number. can be only between 1-10                                      |
| status            | ENUM         | DEFAULT NEW ENUM(NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED) | the mission status. can be only from the list.                                                  |
| risk_level        | ENUM         | ENUM(LOW, MEDIUM, HIGH, CRITICAL)                                          | the system calculate the risk level automatically by `difficulty * 2 + importance = risk_level` |
| assigned_agent_id | INT          |                                                                            | if assigned, will show to which agent. NULL if not assigned.                                    |

---

## Classes structure:

### Class ConnectionDB:

This class is in charge of creating the connection to the databae and build the structure of the program.

#### Methods:
* ```get_connection()``` - return an instance connector.
* ```create_database()``` - builds the database.
* ```create_tables()``` - builds the agents and missions tables.

---

### Class AgentDB:

This class is in charge of all the connections with the agents table.

#### Methods:
* ```create_agent(data)``` - create a new agent from the data insert. Returns the agent dict.
* ```get_all_agents()``` - returns list of all agents. 
* ```get_agent_by_id(id)``` - returns agent dict. None if not exist.
* ```update_agent(id, data)``` - update the agent with the new data.
* ```update_agent(id, data)``` - update the agent with the new data.
* ```deactivate_agent(id)``` - sets the agent as not active.
* ```increment_completed(id)``` - update the number of completed missions.
* ```increment_failed(id)``` - update the number of failed missions.
* ```get_agent_performance(id)``` - returns a dict {"completed", "failed", "total", "success_rate"}.
* ```agents_active_count()``` - count how many agents are active.

---

### Class MissionDB:

This class is in charge of all the connections with the missions table.

#### Methods:
* ```create_mission(data)``` - create a new mission from the data insert. Returns the mission dict.
* ```get_all_missions()``` - returns a list with all missions.
* ```get_mission_by_id(id)``` - returns the mission dict. None if not exist.
* ```assign_mission(m_id, a_id)``` - assigned a mission to an agent.
* ```update_mission_status(id, status)``` - update mission status.
* ```get_open_missions_by_agent(id)``` - returns agent missions that are ASSIGNED/IN_PROGRESS.
* ```count_all_missions()``` - counts all missions. returns a number.
* ```count_by_status(status)``` - counts all missions in certain status. returns a number.
* ```count_open_missions()``` - counts all missions that open and not failed or completed. returns a number.
* ```count_critical_missions()``` - counts all missions in "critical" status. returns a number.
* ```get_top_agent()``` - returns the agent with the biggest completed_missions number


---

## system rules:
* agent_rank must be Commander / Senior / Junior
* difficulty and importance  must be number between 1-10
* level_risk is automatically calculated. Not entered by the user
* agent must be active in order to assigned missions to.
* agent can be assigned only with 3 open missions (ASSIGNED/IN_PROGRESS).
* only a commander can be assigned with critical satus missions.
* only a mission with new status can be assigned to.
* can start a mission only if the status is "ASSIGNED". changes to "IN_PROGRESS".
* can finish a mission (COMPLETED or FAILED) only if the atatus is "IN_PROGRESS".  
* can cancel a mission (to status CANCELLED) only in ASSIGNED or NEW status.

---

## Technologies used:

* python
* docker
* mysql


## User instruction:

* make sure that docker and python are installed.
* using cmd/bash/ect., clone the project using the code: ```git clone https://github.com/MMCohen/IntelligenceTaskManager.git```
* open docker and pull mysql container using the code (using cmd/bash): ```docker pull mysql:8.0```
* build docker container using the code: ```docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0```
* make sure the container runs using ```docker ps``` and search for `intelligence-mysql`. if you dont see it, run the code: ```docker start intelligence-mysql```.
* only if you want the enter to the my sql database use ```docker exec -it intelligence-mysql mysql -uroot -p1234```.
* install required python packages using the code ```pip install mysql-connector-python```
* in this stage of the project (we don't have main.py yet) you will have to enter to each file manually. so first run the connectionDB file, and than continue to the desire file (for missions mission_db and for agents agent_db)




