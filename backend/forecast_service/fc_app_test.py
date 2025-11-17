import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
# Assume your module is named mymodule.py and contains these functions:
# from mymodule import processMessage
load_dotenv()

sys.modules['models.ModelRegistry'] = MagicMock()

from fc_app import processMessage
engine = create_engine(os.environ.get("DATABASE_URL"), pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestProcessMessage(unittest.TestCase):
    @patch('fc_app.trainModel')
    @patch('fc_app.forecastModel')
    def test_process_message_with_mocks(self, mock_forecast, mock_train):
        # Arrange: set up the mocks to return fast dummy values
        dbSession = SessionLocal()
        mock_train.return_value = True
        mock_forecast.return_value = {
            "5000-A000::BB1": [
                505, 1010, 1515, 2020, 2525, 3030, 3535, 4040, 4545, 5050, 5555, 6060
            ],
            "5000-A011::BB1": [
                1234, 1573, 2194, 2736, 3125, 3578, 4294, 5678, 5976, 6574, 1234, 7654
            ],
            "5000-A000::BBS2": [
                2522, 2612, 2718, 2345, 2875, 2093, 2000, 2435, 2778, 2122, 2432, 2675
            ],
            "5000-A000::HQ": [
                1222, 1423, 1540, 1789, 1206, 1357, 1338, 2223, 1157, 2323, 1455, 2346
            ]
        }

        # You can now call processMessage and it will use the mocked functions
        message = "dummy message or test input"
        result = processMessage(message, dbSession)

        dbSession.close()

if __name__ == '__main__':
    unittest.main()
