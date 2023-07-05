from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os


class Main:
    def __init__(self):
        self._hub_connection = None
        self.HOST = os.environ.get("APP_HOST", "http://34.95.34.5")
        self.TOKEN = os.environ.get("APP_TOKEN")
        self.TICKETS = os.environ.get("APP_TICKETS", "5")
        self.T_MAX = os.environ.get("APP_MAX_TEMPERATURE", "35")
        self.T_MIN = os.environ.get("APP_MIN_TEMPERATURE", "10")
        self.DATABASE = os.environ.get(
            "APP_DATABASE", "postgresql://postgres:postgres@localhost:5432/postgres"
        )

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()

    def start(self):
        if self.TOKEN is None:
            raise Exception("The token variable is empty.")

        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def onSensorDataReceived(self, data):
        try:
            print(data[0]["date"] + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])
            self.send_temperature_to_fastapi(date, dp)
            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(
            f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}", timeout=5
        )
        details = json.loads(r.text)
        print(details)

    def send_event_to_database(self, timestamp, event):
        try:
            # To implement
            pass
        except requests.exceptions.RequestException:
            # To implement
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
