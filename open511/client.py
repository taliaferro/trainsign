import logging
from urllib.parse import urljoin

import requests

from .holidays import HolidaysResponseSchema
from .stop_monitoring import StopMonitoringResponseSchema


class Open511Client:
    def __init__(
        self,
        url="https://api.511.org",
        api_key=None,
        rate_limit=60,
        limit_remaining=60,
    ):
        if api_key is None:
            logging.warn("No API key provided -- continuing under the assumption we're in a test environment.")
            api_key = "TEST"
        self.url = url
        self.api_key = api_key

        # resets every hour, on the hour
        # these are initial values only -- the actual value is helpfully returned
        # in the response headers of every request
        self.rate_limit = rate_limit
        self.limit_remaining = limit_remaining

    def _api_get(self, endpoint, params, raise_for_status=True):
        params = {k: v for k, v in params.items() if v is not None}
        params.update({"api_key": self.api_key, "format": "json"})
        request_url = urljoin(self.url, endpoint)

        response = requests.get(request_url, params=params)

        if raise_for_status:
            response.raise_for_status()

        # update rate limit awareness
        self.rate_limit = int(response.headers.get("RateLimit-Limit", self.rate_limit))
        self.limit_remaining = int(
            response.headers.get("RateLimit-Remaining", self.limit_remaining)
        )

        # they sometimes return data in `utf-8-sig` encoding and don't mark it correctly
        if response.text[0] == "\ufeff":
            response.encoding = "utf-8-sig"
        return response

    def stop_monitoring(self, agency, stop_code=None):
        params = {"agency": agency, "stop_code": stop_code}
        resp = self._api_get("transit/StopMonitoring", params=params)
        return StopMonitoringResponseSchema().load(resp.json())

    def vehicle_monitoring(self, agency, vehicle_id=None):
        params = {"agency": agency, "vehicle_id": vehicle_id}
        return self._api_get("transit/VehicleMonitoring", params=params).json()

    def operators(self, operator_id=None):
        params = {"operator_id": operator_id}
        return self._api_get("transit/operators", params=params).json()

    def lines(self, operator_id, line_id=None):
        params = {
            "operator_id": operator_id,
            "line_id": line_id
        }
        return self._api_get("transit/lines", params=params).json()

    def stops(
        self,
        operator_id,
        include_stop_areas=None,
        direction_id=None,
        stop_id=None,
        pattern_id=None,
    ):
        params = {
            "operator_id": operator_id,
            "include_stop_areas": include_stop_areas,
            "direction_id": direction_id,
            "stop_id": stop_id,
            "pattern_id": pattern_id,
        }
        return self._api_get("transit/stops", params=params).json()

    def stop_places(self, operator_id, stop_id=None):
        params = {"operator_id": operator_id, "stop_id": stop_id}
        return self._api_get("transit/stopplaces", params=params).json()

    def patterns(self, operator_id, line_id, pattern_id=None):
        params = {
            "operator_id": operator_id,
            "line_id": line_id,
            "pattern_id": pattern_id,
        }
        return self._api_get("transit/patterns", params=params).json()

    def timetable(
        self, operator_id, line_id, includespecialservice=None, exceptiondate=None
    ):
        params = {
            "operator_id": operator_id,
            "line_id": line_id,
            "includespecialservice": includespecialservice,
            "exceptiondate": exceptiondate,
        }
        return self._api_get("transit/timetable", params=params).json()

    def stop_timetable(
        self, operatorref, monitoringref, lineref=None, starttime=None, endtime=None
    ):
        params = {
            "operatorref": operatorref,
            "monitoringref": monitoringref,
            "lineref": lineref,
            "starttime": starttime,
            "endtime": endtime,
        }
        return self._api_get("transit/stoptimetable", params=params).json()

    def holidays(self, operator_id):
        params = {"operator_id": operator_id}
        resp = self._api_get("transit/holidays", params=params)
        return HolidaysResponseSchema().load(resp.json())
