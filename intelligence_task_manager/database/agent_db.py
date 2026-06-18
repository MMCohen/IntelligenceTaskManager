from intelligence_task_manager.database.connection_db import ConnectionDB
from intelligence_task_manager.database.mission_db import MissionDB

connection = ConnectionDB()

mission_db = MissionDB()

class AgentDB:

    def create_agent(self, data: dict) -> dict:
        """
        create a new agent
        :return: the dict of the new agent
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        sql_vals = data["name"], data["specialty"], data["agent_rank"]

        try:
            cursor.execute(f"""
             INSERT INTO agents (name, specialty, agent_rank)
             VALUES (%s, %s, %s)
             ;
             """, sql_vals)
            last_id = cursor.lastrowid
            connector.commit()

            cursor.execute("SELECT * FROM agents WHERE id = %s;", (last_id,))
            new_agent = cursor.fetchone()
            return new_agent

        finally:
            cursor.close()
            connector.close()


    def get_all_agents(self):
        """
        get a list of all agents. empty list if no missions.
        :return:
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM agents;")
            data = cursor.fetchall()
            return data

        finally:
            cursor.close()
            connector.close()


    def get_agent_by_id(self, id: int) -> dict | None:
        """
        :param id: int
        :return: dict of the agent. None if not found
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM agents WHERE id = %s;", (id,))
            data = cursor.fetchone()
            return data

        finally:
            cursor.close()
            connector.close()


    def update_agent(self, id: int, data: dict):
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        # in order to make sure that the user will not change his id from the dict
        # maybe there is a way in mysql to not allow changes
        data["id"] = id

        sql_claus = ", ".join([f"{key} = %s" for key in data.keys()])
        sql_vals = list(data.values()) + [id]

        try:
            cursor.execute(f"""
            UPDATE agents
            SET {sql_claus}
            WHERE id = %s;
            """, sql_vals)

            connector.commit()

            is_update = cursor.rowcount > 0

            return is_update

            if is_update:
                return {"message": f"agent id {id} update successfully"}
            if not is_update:
                return {"message": f"agent id {id} could not be updated"}

        finally:
            cursor.close()
            connector.close()


    def deactivate_agent(self, id: int) -> dict[str, str] | None:
        """
        sets is_active to False by id
        :return: str message
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        try:
            cursor.execute(f"""
            UPDATE agents
            SET is_active = False
            WHERE id = %s;
            """, (id, ))

            connector.commit()

            is_update = cursor.rowcount > 0
            if is_update:
                return {"message": f"agent id {id} deactivate successfully"}
            if not is_update:
                return {"message": f"agent id {id} could not be deactivate"}

        finally:
            cursor.close()
            connector.close()
        return None


    def increment_completed(self, id: int):
        """
        increase the completed_missions by id
        :param id:
        :return:
        """

        agent_data = self.get_agent_by_id(id)

        if not agent_data:
            return "agent doesn't exist"

        agent_completed_missions = agent_data.get("completed_missions", 0)
        update_completed_missions = agent_completed_missions + 1

        connector = connection.get_connection()
        cursor = connector.cursor()

        cursor.execute("""
                    UPDATE agents
                    SET completed_missions = %s
                    WHERE id = %s;""", (update_completed_missions, id))

        connector.commit()
        cursor.close()
        connector.close()

        return "agent increase completed missions successfully"


    def increment_failed(self, id):
            """
            increase agent failed missions
            :param id:
            :return:
            """
            agent_data = self.get_agent_by_id(id)

            if not agent_data:
                return "agent doesn't exist"

            agent_failed_missions = agent_data.get("failed_missions", 0)
            update_failed_missions = agent_failed_missions + 1

            connector = connection.get_connection()
            cursor = connector.cursor()

            cursor.execute("""
            UPDATE agents
            SET failed_missions = %s
            WHERE id = %s;""", (update_failed_missions, id))

            connector.commit()
            cursor.close()
            connector.close()

            return "agent increase failed missions successfully"


    def get_agent_performance(self, id):
        """
        calculate agent performance
        :param id:
        :return:
        """
        agent_data: dict = self.get_agent_by_id(id)
        if agent_data:
            agent_open_missions = mission_db.get_open_missions_by_agent(id)

            completed = agent_data["completed_missions"]
            failed = agent_data["failed_missions"]
            total = completed + failed + len(agent_open_missions)
            success_rate = 100 / total * completed

            return {"completed": completed,
                    "failed": failed,
                    "total": total,
                    "success_rate": success_rate
                    }

        return None


    def count_active_agents(self) -> int:
        """
        count the number of active agents
        :return: int
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute("""
        SELECT COUNT(is_active) as active_agents FROM agents
        WHERE is_active = True;
        """)

        data = cursor.fetchone()

        cursor.close()
        connector.close()

        active_agents = data.get("active_agents", 0)

        return active_agents

    def get_top_agent(self):
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute("""
        SELECT id, name, specialty, is_active, failed_missions, agent_rank, max(completed_missions) as completed_missions  
        FROM agents
        group by id, name, specialty, is_active, failed_missions, agent_rank
        order by completed_missions desc
        limit 1
        ;
        """)

        data = cursor.fetchone()

        cursor.close()
        connector.close()

        return data





if __name__ == "__main__":
    ag = AgentDB()
    # new = {"name": "Moshe", "specialty": "spy", "agent_rank": "Junior"}
    # print(ag.create_agent(new))

    # print(ag.get_all_agents())
    # print(ag.get_agent_by_id(1))
    print(ag.update_agent(3, {"name": "David"}))

    # print(ag.deactivate_agent(4))

    # print(ag.increment_completed(1))

    # print(ag.count_active_agents())

    # print(ag.get_agent_performance(2))

    # print((ag.increment_failed(2)))

    # print(ag.get_top_agent())