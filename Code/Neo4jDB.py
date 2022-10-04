from neo4j import GraphDatabase
from datetime import datetime, timedelta
import pandas as pd
import json
import re


class Neo4jDB:

    def __init__(self, uri, user, password):
        """
        Sets up driver instance to connect to neo4j database.
        :param uri: connection string
        :param user, password: user credentials
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Closes driver instance.
        """
        self.driver.close()

    def get_csv(self, config_path, force_default_time=False):
        """
        Saves csv containing data retrieved by query.
        :param config_path: path of config file
        :param force_default_time: controls whether to use default time
        """
        with open(config_path) as cfg:
            config = json.load(cfg)

        # Get database query and name of file to be saved
        query = config["query"]
        filename = config["filename"]

        # Get time when query was last performed
        last_updated = self._read_log_time(config_path, force_default_time)

        # Adapt query with time of last update
        if re.search(r"%DATETIME%", query):
            query = query.replace("%DATETIME%", f"'{last_updated}'")

        # Open driver session and run query, save result at specified path
        with self.driver.session() as session:
            data = session.read_transaction(self._perform_query, query)
            df = pd.DataFrame(data)
            df.to_csv("../Data" + filename)

    def write_from_query(self, query):
        """
        Writes to database from query
        :param query: query specification
        """
        with self.driver.session() as session:
            session.write_transaction(self._perform_query, query)

    @staticmethod
    def _perform_query(tx, query):
        """
        :param tx: neo4j transaction object.
        :param query: query specification
        :return: retrieved data
        """
        result = tx.run(query)
        return result.data()

    @staticmethod
    def _read_log_time(config_path, force_default_time=False, buffer=15):
        """
        Read time from config file and log current time minus some buffer in minutes
        :param config_path: path to config file
        :param force_default_time: controls whether to use default time
        """

        try:
            with open(config_path, "r") as f:
                config = json.load(f)

            # Get current time and subtract buffer
            current_time = datetime.today() - timedelta(minutes=buffer)
            current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")

            if not force_default_time and re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", config["last_updated"]):
                last_updated = config["last_updated"]
            else:
                last_updated = config["default_time"]

            # Log current time as time of last update in config file
            config["last_updated"] = current_time
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)

        # In case of error, use below default time as fallback
        except (Exception, ):
            last_updated = "2000-01-01T00:00:00"

        return last_updated
