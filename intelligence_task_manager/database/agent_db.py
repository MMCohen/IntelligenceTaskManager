from intelligence_task_manager.database.connection_db import ConnectionDB

connection = ConnectionDB()

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
            if is_update:
                return {"message": f"agent id {id} update successfully"}
            if not is_update:
                return {"message": f"agent id {id} could not be updated"}

        finally:
            cursor.close()
            connector.close()


    def deactivate_agent(self, id):
        pass


    def increment_completed(self, id):
        pass


    def increment_failed(self, id):
        pass


    def get_agent_performance(self, id):
        pass


    def agents_active_count(self):
        pass


if __name__ == "__main__":
    ag = AgentDB()
    # new = {"name": "Moshe", "specialty": "spy", "agent_rank": "Junior"}
    # print(ag.create_agent(new))

    # print(ag.get_all_agents())
    # print(ag.get_agent_by_id(1))
    print(ag.update_agent(3, {"name": "David"}))
