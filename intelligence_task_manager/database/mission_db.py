from intelligence_task_manager.database.connection_db import ConnectionDB

connection = ConnectionDB()

class MissionDB:

    MAX_OPEN_MISSIONS_PER_AGENT = 3

    def create_mission(self, data: dict) -> dict:
        """
        add new mission to the database
        :param data:
        :return:
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        # sql_fields = ", ".join([f"{key}" for key in data.keys()])
        # sql_place_holders = "%s, " * len(data)
        # sql_vals = list(data.values())

        risk_level = self.calculate_risk_level(data["difficulty"], data["importance"])

        sql_vals = data["title"], data["description"], data["location"], data["difficulty"], data["importance"], risk_level

        try:
            cursor.execute(f"""
            INSERT INTO missions (title, description, location, difficulty, importance, risk_level)
            VALUES (%s, %s, %s, %s, %s, %s)
            ;
            """, sql_vals)
            last_id = cursor.lastrowid
            connector.commit()

            cursor.execute("SELECT * FROM missions WHERE id = %s;", (last_id, ))
            new_mission = cursor.fetchone()
            return new_mission

        finally:
            cursor.close()
            connector.close()


    def calculate_risk_level(self, difficulty: int, importance: int) -> str | None:
        """
        calculate risk level using the formula (difficulty * 2) + importance
        """
        risk_level = (difficulty * 2) + importance

        if 1 <= risk_level <= 9:
            return "LOW"
        elif 10 <= risk_level <= 17:
            return "MEDIUM"
        elif 18 <= risk_level <= 24:
            return "HIGH"
        elif 25 <= risk_level:
            return "CRITICAL"


    def get_all_missions(self) -> list[dict | None]:
        """
        get all missions. empty list if no missions.
        :return:
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM missions;")
            data = cursor.fetchall()
            return data

        finally:
            cursor.close()
            connector.close()


    def get_mission_by_id(self, id: int) -> dict | None:
        """
        :param id: int
        :return: dict of the mission. None if not found
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM missions WHERE id = %s;", (id,))
            data = cursor.fetchone()
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


    def assign_mission(self, m_id, a_id):
        """
        assign_mission to agent
        :return:
        """
        agent_data = self.get_agent_by_id(a_id)
        mission_data = self.get_mission_by_id(m_id)
        agent_open_missions = self.get_open_missions_by_agent(a_id)
        number_of_agent_missions = len(agent_open_missions)

        if not agent_data or agent_data["is_active"] == False:
            return "agent not exist or not active"

        if not mission_data or mission_data["status"].lower() != "new":
            return "mission not found or cannot be assigned"

        if number_of_agent_missions >= MissionDB.MAX_OPEN_MISSIONS_PER_AGENT:
            return "agent already assigned maximum missions"

        if mission_data["risk_level"].lower() == "critical" and agent_data["agent_rank"].lower() != "commander":
            return "agent must be a commander in order to assigned critical missions"

        mission_data["status"] = "ASSIGNED"
        mission_data["assigned_agent_id"] = a_id

        connector = connection.get_connection()
        cursor = connector.cursor()

        sql_claus = ", ".join([f"{key} = %s" for key in mission_data.keys()])
        sql_vals = list(mission_data.values()) + [m_id]

        cursor.execute(f"""
        UPDATE missions
        SET {sql_claus}
        WHERE id = %s;""", sql_vals)

        connector.commit()
        cursor.close()
        connector.close()
        return "assign successfully"


    def update_mission_status(self, id: int, status: str):
        mission_data = self.get_mission_by_id(id)
        mission_status = mission_data["status"]
        update_staus = status

        if mission_status.lower() == "new" and update_staus.lower() != "assigned":
            return "cannot change"
        if mission_status.lower() == "assigned" and update_staus.lower() in ("NEW", "ASSIGNED", "COMPLETED", "CANCELLED"):
            return "cannot change"
        if mission_status.lower() == "in_progress" and update_staus.lower() not in ("failed", "completed"):
            return "cannot change"

        mission_data["status"] = update_staus

        connector = connection.get_connection()
        cursor = connector.cursor()

        cursor.execute("""
        UPDATE missions
        SET status = %s
        WHERE id = %s;""",(update_staus, id))

        connector.commit()
        cursor.close()
        connector.close()

        return "update success"


    def get_open_missions_by_agent(self, id):
        """
        returns list with ASSIGNED or IN_PROGRESS by id
        :param id:
        :return:
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)
        try:
            cursor.execute("""
            SELECT * FROM missions
            WHERE assigned_agent_id = %s AND status = "ASSIGNED" OR status = "IN_PROGRESS";
            """, (id, ))

            open_missions = cursor.fetchall()

        finally:
            cursor.close()
            connector.close()

        return open_missions


    def count_all_missions(self):
        """
        count all missions
        :return: int
        """
        all_missions = self.get_all_missions()
        return len(all_missions)


    def count_by_status(self, status: str) -> int:
        """
        count missions by status
        :param status: str
        :return: int
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)
        try:
            cursor.execute("""
                            SELECT COUNT(*) as count_by_status FROM missions
                            WHERE status = %s;
                            """, (status, ))

            count_by_status = cursor.fetchone()

        finally:
            cursor.close()
            connector.close()

        return count_by_status["count_by_status"]


    def count_open_missions(self) -> int:
        """
        count open missions
        :return: int
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)
        try:
            cursor.execute("""
                    SELECT COUNT(*) as open_missions FROM missions
                    WHERE status = "ASSIGNED" OR status = "IN_PROGRESS";
                    """)

            open_missions = cursor.fetchone()

        finally:
            cursor.close()
            connector.close()

        return open_missions["open_missions"]


    def count_critical_missions(self) -> int:
        """
        count missions with risk level = critical
        :return: int
        """
        connector = connection.get_connection()
        cursor = connector.cursor(dictionary=True)
        try:
            cursor.execute("""
                            SELECT COUNT(*) as critical_missions FROM missions
                            WHERE risk_level = "critical";
                            """)

            critical_missions = cursor.fetchone()

        finally:
            cursor.close()
            connector.close()

        return critical_missions["critical_missions"]


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
    mis = MissionDB()
    # new_mis = {"title": "title", "description": "dfsdf" , "location": "dfsdf", "difficulty": 6, "importance": 6, "risk_level": "low"}
    # print(mis.create_mission(new_mis))
    # print(mis.get_all_missions())
    # print(mis.get_mission_by_id(1))

    # print(mis.get_open_missions_by_agent(2))
    # print(mis.count_open_missions())
    # print(mis.count_critical_missions())
    # print(mis.count_all_missions())
    # print(mis.assign_mission(5, 6))
    # print(mis.update_mission_status(2, "in_progress"))
    print(mis.get_top_agent())