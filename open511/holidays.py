"""
Wrote this to test out the Marshmallow serializer. Holidays aren't used in the app,
but the holiday response data structure is the simplest.
"""

from .base_schema import BaseSchema  # returns a Namespace instead of a dict
from marshmallow import fields


class AvailabilityConditionSchema(BaseSchema):
    version = fields.Str(data_key="version")
    id = fields.Str(data_key="id")
    from_date = fields.AwareDateTime(data_key="FromDate")
    to_date = fields.AwareDateTime(data_key="ToDate")


class ServiceCalendarSchema(BaseSchema):
    id = fields.Str(data_key="id")
    from_date = fields.Date("%Y-%m-%d", data_key="FromDate")
    to_date = fields.Date("%Y-%m-%d", data_key="ToDate")


class HolidaysContentSchema(BaseSchema):
    service_calendar = fields.Nested(ServiceCalendarSchema, data_key="ServiceCalendar")
    availability_conditions = fields.List(
        fields.Nested(AvailabilityConditionSchema), data_key="AvailabilityConditions"
    )


class HolidaysResponseSchema(BaseSchema):
    content = fields.Nested(HolidaysContentSchema, data_key="Content")
