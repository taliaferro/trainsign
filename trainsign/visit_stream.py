from datetime import datetime
import asyncio


async def visit_stream(
    client, agency, stop_code=None, meter=True, rate_limit_overhead=0
):
    while True:
        data = client.stop_monitoring(agency, stop_code=stop_code)
        visits = data.service_delivery.stop_monitoring_delivery.monitored_stop_visit
        for visit in visits:
            yield visit

        if meter:
            now = datetime.now()
            reset_time = datetime(
                now.year, now.month, now.day, now.hour + 1, tzinfo=now.tzinfo
            )
            time_till_reset = (reset_time - now).seconds
            await asyncio.sleep(
                time_till_reset / (client.limit_remaining + rate_limit_overhead)
            )
