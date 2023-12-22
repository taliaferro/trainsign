from datetime import datetime
import asyncio

from marshmallow import Schema, fields, post_load
from .visit_schema import VisitSchema


class ArrivalsState:
    def __init__(self, client, agency: str, meter=True, rate_limit_overhead=0):
        self.visits = {}
        self.client = client
        self.agency = agency
        self.meter = meter
        self.rate_limit_overhead = rate_limit_overhead
        self.schema = VisitSchema(many=True)

    async def poll(self):
        while True:
            raw_data = self.client.stop_monitoring(self.agency)
            arrivals = raw_data["ServiceDelivery"]["StopMonitoringDelivery"][
                "MonitoredStopVisit"
            ]
            self.arrivals = self.schema.load(arrivals)

            if self.meter:
                now = datetime.now()
                reset_time = datetime(
                    now.year, now.month, now.day, now.hour + 1, tzinfo=now.tzinfo
                )
                time_till_reset = (reset_time - now).seconds
                await asyncio.sleep(
                    time_till_reset
                    / (self.client.limit_remaining + self.rate_limit_overhead)
                )

    def query(self, line: str = None, direction: str = None, stop: int = None):
        def arrival_match(a: dict):
            if a["journey"]["direction"] != direction:
                return False
            if a["journey"]["line_ref"] != line:
                return False
            if a["journey"]["status"]["stop_ref"] != stop:
                return False
            return True

        return filter(self.arrivals, arrival_match).sort(
            lambda a: a["journey"]["status"]["expected_arrival_time"]
        )
