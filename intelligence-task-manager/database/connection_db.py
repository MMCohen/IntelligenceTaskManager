import mysql.connector
from mysql.connector.aio import connect


class ConnectionDB:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = "Intelligence_db"


    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )


    def create_database(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db;")

        connection.commit()
        cursor.close()
        connection.close()


    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        table_agents = """
        CREATE TABLE IF NOT EXISTS agents(
        
 id                  INT          AUTO_INCREMENT PRIMARY KEY NOT NULL,        
 name                VARCHAR(50)  NOT NULL,                       
 specialty           VARCHAR(50)  NOT NULL,        
 is_active           BOOLEAN NOT NULL	     DEFAULT TRUE,       
 completed_missions  INT NOT NULL         DEFAULT 0,
 failed_missions     INT NOT NULL          DEFAULT 0,    
 agent_rank          ENUM('Junior', 'Senior', 'Commander') NOT NULL
        );
        """

        table_missions = """
               CREATE TABLE IF NOT EXISTS missions(

        id                  INT          AUTO_INCREMENT PRIMARY KEY NOT NULL,        
        title               VARCHAR(255)  NOT NULL,        
        description         TEXT NOT NULL,       
        location            VARCHAR(255) NOT NULL,
        difficulty          INT NOT NULL          CHECK (difficulty > 0 and difficulty < 11),  
        importance          INT NOT NULL          CHECK (importance > 0 and importance < 11),    
        status              ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') NOT NULL DEFAULT 'NEW',
        risk_level          ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')  NOT NULL,        
        assigned_agent_id   INT        
               );
               """

        cursor.execute(table_agents)
        cursor.execute(table_missions)
        # cursor.execute("""
        # insert into missions(title, description, location, difficulty, importance, risk_level)
        # values ("try", "desc", "loca", 3, 5, "low")
        # ;""")

        connection.commit()
        cursor.close()
        connection.close()



if __name__ == "__main__":
    con = ConnectionDB()
    con.create_database()


