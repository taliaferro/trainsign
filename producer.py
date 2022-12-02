from datetime import datetime
import asyncio


async def visit_data_stream(
    self, client, agency, stop_code=None, meter=True, rate_limit_overhead=0
):
    while True:
        data = client.stop_monitoring(agency, stop_code=stop_code)
        stop_states = data["ServiceDelivery"]["StopMonitoringDelivery"][
            "MonitoredStopVisit"
        ]
        for state in stop_states:
            yield state

        if meter:
            now = datetime.now()
            reset_time = datetime(
                now.year, now.month, now.day, now.hour + 1, tzinfo=now.tzinfo
            )
            time_till_reset = (reset_time - now).seconds
            await asyncio.sleep(time_till_reset / (client.limit_remaining + rate_limit_overhead))
