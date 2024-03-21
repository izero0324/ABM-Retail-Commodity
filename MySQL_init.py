import json
import os
import subprocess
import sys

def is_mysql_installed():
    try:
        subprocess.check_output("mysql --version", shell=True)
        return True
    except subprocess.CalledProcessError:return False

def install_mysql_mac():
    print("Attempting to install MySQL on MacOS...")
    os.system("brew update && brew install mysql")
    os.system("brew services start mysql")
    print("MySQL has been installed and started.")

def install_mysql_windows():
    print("Automatic MySQL installation is not supported on Windows.")
    print("Please download and install MySQL from: https://dev.mysql.com/downloads/mysql/")
    print("After installation, run this script again.")

def create_database(user, password):
    try:
        subprocess.check_output(f'mysql -u {user} -p{password} -e "CREATE DATABASE IF NOT EXISTS ABM_EXCHANGE;"', shell=True)
        print("Database 'ABM_EXCHANGE' created successfully.")
    except subprocess.CalledProcessError as e:
        print("Could not create database. Error:", e.output)

def create_config(user, password):
    config = {
        "MySQL": {
            "type": "mysql",
            "user": user,
            "password": password,
            "host": "localhost",
            "database": "ABM_EXCHANGE",
            "raise_on_warnings": True
        }
    }
    if not os.path.exists("tools"):
        os.makedirs("tools")
    with open("tools/sql_config.json", "w") as json_file:
        json.dump(config, json_file, indent=4)
    print("Configuration file 'sql_config.json' has been created under 'tools' folder.")

if __name__ == "__main__":
    if not is_mysql_installed():
        if sys.platform == "darwin":  # MacOS
            install_mysql_mac()
        elif sys.platform.startswith("win"):  # Windows
            install_mysql_windows()
    else:
        print("MySQL is already installed.")

    # Prompt user for MySQL root user and password to create database and config file
    user = input("Enter MySQL root user: ")
    password = input("Enter MySQL password: ")
    create_database(user, password)
    create_config(user, password)