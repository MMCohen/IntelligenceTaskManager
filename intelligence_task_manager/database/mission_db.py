from intelligence_task_manager.database.connection_db import ConnectionDB

connection = ConnectionDB()

class MissionDB:
    pass

    def create_mission(self, data):
        pass


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
        pass


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
    print(mis.get_all_missions())

