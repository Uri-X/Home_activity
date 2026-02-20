import fabric
import datetime
from fabric import Connection

with open('fabric_activity/password.txt') as f:
    password = f.read().strip()

# Connecting to localhost as my user
connection = Connection(
    host = '127.0.0.1',
    user = 'BabyBoy',
    connect_kwargs = {'password': password}
)

time_mod = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def install_mysql():
    # Installation of mysql server
    connection.run("sudo apt-get update -y")
    connection.run("sudo apt-get install -y mysql-server")

def create_database(db_name="taxi_zone_db"):
    # Creation of database
    connection.run(f"sudo mysql -e 'CREATE DATABASE IF NOT EXISTS {db_name};'")

def load_taxi_data(db_name="taxi_zone_db", dump_path=r"C:\Users\user\Desktop\Home_activity\fabric_activity\taxi_zone_lookup (1).sql"):
    # Loading Taxi Zone dump
    connection.run(
        f"sudo mysql {db_name} < '{dump_path}'"
    )

def setup_mysql():
    #Running the commands
    install_mysql()
    create_database("taxi_zone_db")
    load_taxi_data("taxi_zone_db", r"C:\Users\user\Desktop\Home_activity\fabric_activity\taxi_zone_lookup (1).sql")

setup_mysql()