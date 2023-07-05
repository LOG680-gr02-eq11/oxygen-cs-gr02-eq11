import unittest
from src.main import Main
import os


class MainTests(unittest.TestCase):
    def test_default_values(self):
        main = Main()
        self.assertEqual(main.HOST, "http://34.95.34.5")
        self.assertEqual(main.TOKEN, "0FagpkvF4B")
        self.assertEqual(main.TICKETS, "5")
        self.assertEqual(main.T_MAX, "35")
        self.assertEqual(main.T_MIN, "10")
        self.assertEqual(
            main.DATABASE, "postgresql://postgres:postgres@localhost:5432/postgres"
        )

    def test_custom_values(self):
        # Set the environment variables with custom values for testing
        os.environ["APP_HOST"] = "http://34.95.34.5"
        os.environ["APP_TOKEN"] = "0FagpkvF4B"
        os.environ["APP_TICKETS"] = "10"
        os.environ["APP_MAX_TEMPERATURE"] = "40"
        os.environ["APP_MIN_TEMPERATURE"] = "5"
        os.environ[
            "APP_DATABASE"
        ] = "postgresql://postgres:postgres@localhost:5432/postgres"

        main = Main()
        self.assertEqual(main.HOST, "http://34.95.34.5")
        self.assertEqual(main.TICKETS, "10")
        self.assertEqual(main.T_MAX, "40")
        self.assertEqual(main.T_MIN, "5")
        self.assertEqual(
            main.DATABASE, "postgresql://postgres:postgres@localhost:5432/postgres"
        )


if __name__ == "__main__":
    unittest.main()
