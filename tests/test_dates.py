import unittest
from datetime import datetime
from unittest.mock import patch

from core.dates import (
    forecast_hour,
    format_valid_time,
    get_valid_time,
)


class DatesTest(unittest.TestCase):
    @patch("core.dates.get_start_valid_time")
    def test_timestep_one_is_lead_hour_zero(self, get_start_valid_time):
        get_start_valid_time.return_value = datetime(2026, 6, 10)

        self.assertEqual(get_valid_time(1), datetime(2026, 6, 10))
        self.assertEqual(forecast_hour(1), 0)

    @patch("core.dates.get_start_valid_time")
    def test_formatted_valid_time_contains_utc_once(self, get_start_valid_time):
        get_start_valid_time.return_value = datetime(2026, 6, 10)

        valid_time = format_valid_time(1)

        self.assertEqual(valid_time, "2026-06-10 00:00 UTC")
        self.assertEqual(valid_time.count("UTC"), 1)


if __name__ == "__main__":
    unittest.main()
