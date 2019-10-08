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

        def run(self):
            """Executes the program"""
            # Get FitBit data
            # https://api.fitbit.com/1/user/223VS85/sleep/date/2019-10-07.json

            print("todo")

            # Get air quality data
            print("todo")

            # Convert data for ocs
            print("todo")

            # Write to ocs
            print("todo")

    def test2(self):
        return

    def WriteToSds(self, data):
        # fbType = self.sds.init_type("FitBitType", ["Time", "SleepHours"])
        self.sds.to_sds(data,)
        self.sds.client.get_or_create_type(self.sds.namespace_id)

    def test(self):
        fb = FitBit(self.config)
        data = fb.get_sleep_data("2019-10-07")
        self.WriteToSds(data)
        # sdsType = self.sds.init_type
        print("")


def main():
    """Application's entry point"""
    config = ConfigParser()
    config.read("./config.ini")
    app = Program(config)
    # app.run()
    app.test()
    # app.test2()


if __name__ == "__main__":
    main()
