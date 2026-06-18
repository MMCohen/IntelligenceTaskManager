from intelligence_task_manager.database.connection_db import ConnectionDB

connection = ConnectionDB()

class MissionDB:

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


    def assign_mission(self, m_id, a_id):
        pass


    def update_mission_status(self, id, status):
        pass


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
        pass


    def count_by_status(self, status):
        pass


    def count_open_missions(self):
        pass


    def count_critical_missions(self):
        pass


    def get_top_agent(self):
        pass


if __name__ == "__main__":
    mis = MissionDB()
    # new_mis = {"title": "title", "description": "dfsdf" , "location": "dfsdf", "difficulty": 6, "importance": 6, "risk_level": "low"}
    # print(mis.create_mission(new_mis))
    # print(mis.get_all_missions())
    # print(mis.get_mission_by_id(1))

    print(mis.get_open_missions_by_agent(2))

