import json
import requests
from datetime import datetime
from datetime import timedelta
from sdspy import *


class Program:
    """Dfines the main wrapper class"""
    def __init__(self, config):
        """
        config: parameters from local config.ini
        """
        print("------------------------------------------")
        print("  _________    .___     __________        ")
        print(" /   _____/  __| _/_____\______   \___.__.")
        print(" \_____  \  / __ |/  ___/|     ___<   |  |")
        print(" /        \/ /_/ |\___ \ |    |    \___  |")
        print("/_______  /\____ /____  >|____|    / ____|")
        print("        \/      \/    \/           \/     ")
        print("------------------------------------------")
        print()
        self.config = config
        self.sds = SequentialDataStore(self.config)
        self.fitbit = FitBit(self.config)

    def run(self):
        """Executes the program"""
        # Get FitBit data
        fitbit_sleep_data = self.fitbit.get_sleep_data(self.config.get("Preferences", "StartDate"))["sleep"][0]

        # Get air quality data
        print("todo: GET AIR QUALITY DATA")

        # Convert & Write to ocs
        # TODO: loop for all datapoints
        start_date_from_fitbit_str = fitbit_sleep_data["startTime"]

        sds_date_format = '%Y-%m-%dT%H:%M:%S.000'
        fitbit_date_format = '%Y-%m-%d'
        # 2019-10-08T21:47:30.000
        # start_date_from_fitbit_obj = datetime.strptime(start_date_from_fitbit_str, sds_date_format)

        current_date_from_config_str = self.config.get("Preferences", "StartDate")
        end_date_from_config_str = self.config.get("Preferences", "EndDate")
        end_date_from_config_obj = datetime.strptime(end_date_from_config_str, fitbit_date_format)
        current_date_from_config_obj = datetime.strptime(current_date_from_config_str, fitbit_date_format)

        while current_date_from_config_obj <= end_date_from_config_obj:
            # Get FitBit data
            fitbit_sleep_data = self.fitbit.get_sleep_data(current_date_from_config_str)["sleep"][0]
            self.sds.to_sds("sleep", current_date_from_config_str, fitbit_sleep_data["minutesAsleep"])

            current_date_from_config_obj += timedelta(days=1)
            current_date_from_config_str = datetime.strftime(current_date_from_config_obj, '%Y-%m-%d')
            sleep(24)

        # cleanup(self.sds.client, self.sds.namespace_id, ["sleeptype"])


def main():
    """Application's entry point"""
    config = ConfigParser()
    config.read("./config.ini")
    app = Program(config)
    # app.test()
    app.run()
    print("Ok!")


if __name__ == "__main__":
    main()
