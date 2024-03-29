import json
import sqlite3
import mysql.connector
from mysql.connector import errorcode

def load_sql_config(config_file='tools/sql_config_s.json'):
    '''
    Get sql configs from json
    '''
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config['MySQL'] #change here for other DBs

class DatabaseConnectionManager:
    def __init__(self):
        self.config = load_sql_config()
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

def create_or_truncate_tables(cursor, experiment_name):
    # Construct new tables for new experiment names
    OrderBook_table = 'OrderBook_' + experiment_name
    PriceSpread_table = 'PriceSpread_' + experiment_name
    SuccessTrade_table = 'SuccessTrade_' + experiment_name
    LOB_table = 'LOB_' + experiment_name
    
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
        ),
        f"{LOB_table}":(
            f"CREATE TABLE IF NOT EXISTS {LOB_table} ("
            "  `tick` int,"
            "  `price` float,"
            "  `quantity` float,"
            "  `side` VARCHAR(255)"
            ") "
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
        

