import json
import requests
from sdspy import *


class Program:
    """Dfines the main wrapper class"""
    def __init__(self, config):
        """
        config: parameters from local config.ini
        ws: contains attributes related to La Crosse View weather station
        sds: contains attributes related to Sequential Data Store (SDS)
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
        sleep_info = self.fitbit.get_sleep_data(self.config.get("Preferences", "StartDate"))["sleep"][0]

        # Get air quality data
        print("todo: GET AIR QUALITY DATA")

        # Convert & Write to ocs
        # TODO: loop for all datapoints
        self.sds.to_sds("FitBit", sleep_info["startTime"], sleep_info["duration"])


def main():
    """Application's entry point"""
    config = ConfigParser()
    config.read("./config.ini")
    app = Program(config)
    app.run()
    print("Ok!")


if __name__ == "__main__":
    main()
