from datetime import datetime
import asyncio

class VisitStream():
    def __init__(self, client, agency, meter=True, rate_limit_overhead=0):
        self.visits = {}
        self.client=client
        self.agency=agency
        self.meter=meter
        self.rate_limit_overhead=rate_limit_overhead

    async def stream(self):
        while(True):
            data = self.client.stop_monitoring(self.agency)
            self.visits = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
            if self.meter:
                now = datetime.now()
                reset_time = datetime(
                    now.year, now.month, now.day, now.hour + 1, tzinfo=now.tzinfo
                )
                time_till_reset = (reset_time - now).seconds
                await asyncio.sleep(
                    time_till_reset / (self.client.limit_remaining + self.rate_limit_overhead)
                )
