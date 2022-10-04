import os
import argparse
import logging
from Neo4jDB import Neo4jDB
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s;%(levelname)s;%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config_file", type=str, required=True, help="config file path", default="config.json")
parser.add_argument("-f", "--force", action="store_true", help="Use default time specified in config")

args = parser.parse_args()

config_path = args.config_file
force_default_time = args.force

load_dotenv()

logging.info("Creating Neo4jDB instance")

db = Neo4jDB(uri=os.getenv("URI"),
             user=os.getenv("USERNAME"),
             password=os.getenv("PASSWORD"))

logging.info("Saving csv file")

db.get_csv(config_path, force_default_time=force_default_time)