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


    def get_agent_by_id(self, id):
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


    def update_agent(self, id, data):
        pass


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
