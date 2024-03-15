import sqlite3
import mysql.connector
from mysql.connector import errorcode

class DatabaseConnectionManager:
    def __init__(self):
        self.config ={
            'type': 'mysql',
            'user': 'root',
            'password': '********', 
            'host': 'localhost',
            'database': 'ABM_EXCHANGE',
            'raise_on_warnings': True
        }
        '''
        for sqlite, change the config to 
        {
            'type': 'sqlite',
            'db_file': 'example.db'
        }
        '''
        self.connection = None
        self.cursor = None

    def __enter__(self):
        db_type = self.config.get('type')
        
        try:
            if db_type == 'sqlite':
                self.connection = sqlite3.connect(self.config.get('db_file'))
            elif db_type == 'mysql':
                mysql_config = {key: value for key, value in self.config.items() if key != 'type'}
                self.connection = mysql.connector.connect(**mysql_config)
            else:
                raise ValueError("Unsupported database type specified.")
                
            self.cursor = self.connection.cursor()
            return self.cursor
        except (sqlite3.Error, mysql.connector.Error) as err:
            print(f"Error connecting to {db_type.upper()} database: {err}")
            exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if not exc_type and self.config.get('type') == 'mysql':
                # Only commit if no exceptions and database is MySQL
                self.connection.commit()
                
            self.cursor.close()
            self.connection.close()
        if exc_type:
            print(f"Error: {exc_val}")


class SQLiteConnectionManager:
    def __init__(self, db_file):
        # Specify your SQLite database file name here
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as err:
            print(f"Error connecting to SQLite: {err}")
            exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if not exc_type:
                # Only commit if no exceptions
                self.connection.commit()
            self.cursor.close()
            self.connection.close()
        if exc_type:
            print(f"Error: {exc_val}")

class MySQLConnectionManager:
    def __init__(self):
        # Remember to change the configs below!!!
        self.config = {
            "user": "root",
            "password": "********", 
            "host": "localhost",
            "database": "ABM_EXCHANGE",
            "raise_on_warnings": True
        }
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        if exc_type:
            print(f"Error: {exc_val}")

def create_or_truncate_tables(cursor, experiment_name):
    # Construct new tables for new experiment names
    OrderBook_table = 'OrderBook_' + experiment_name
    PriceSpread_table = 'PriceSpread_' + experiment_name
    SuccessTrade_table = 'SuccessTrade_' + experiment_name
    
    # SQLs for Creating TABLES
    TABLES = {

        f"{OrderBook_table}": (
            f"CREATE TABLE IF NOT EXISTS {OrderBook_table} ("
            "  `tick` int,"
            "  `agent_name` VARCHAR(255), "
            "  `trade_price` float,"
            "  `quantity` float"
            ") "
        ),
        
        f"{PriceSpread_table}": (
            f"CREATE TABLE IF NOT EXISTS {PriceSpread_table} ("
            "  `tick` int,"
            "  `LowestSuccessTradePrice` float,"
            "  `HighestSuccessTradePrice` float"
            ")"
        ),
        f"{SuccessTrade_table}": (
            f"CREATE TABLE IF NOT EXISTS {SuccessTrade_table} ("
            "  `tick` int,"
            "  `buy_agent` VARCHAR(255), "
            "  `sell_agent` VARCHAR(255),"
            "  `trade_price` float,"
            "  `quantity` float"
            ")"
        )

    }

    # Execute creating table one-by-one
    for table_name, table_description in TABLES.items():
        try:
            cursor.execute(table_description)
            print(f"Table {table_name} checked/created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating/checking table {table_name}: {err.msg}")
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        

