from datetime import timedelta
from sdspy import *


class Program:
    """Defines the main wrapper class"""
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
        fitbit_date_format = '%Y-%m-%d'

        current_date_str = self.config.get("Preferences", "StartDate")
        current_date = datetime.strptime(current_date_str, fitbit_date_format)
        end_date = datetime.strptime(self.config.get("Preferences", "EndDate"), fitbit_date_format)
        frequency = int(self.config.get("Preferences", "Frequency"))

        while current_date <= end_date:
            # Get FitBit sleep data and write to SDS
            fitbit_sleep_data = self.fitbit.get_sleep_data(current_date_str)["sleep"][0]
            self.sds.to_sds("sleep", current_date_str, fitbit_sleep_data["minutesAsleep"])

            # increment by 1 day
            current_date += timedelta(days=1)
            current_date_str = datetime.strftime(current_date, fitbit_date_format)

            sleep(frequency)


def main():
    """Application's entry point"""
    config = ConfigParser()
    config.read("./config.ini")
    app = Program(config)
    app.run()


if __name__ == "__main__":
    main()
