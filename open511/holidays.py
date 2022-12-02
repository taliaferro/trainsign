"""
Wrote this to test out the Marshmallow serializer. Holidays aren't used in the app,
but the holiday response data structure is the simplest.
"""

from .base_schema import BaseSchema  # returns a Namespace instead of a dict
from marshmallow import fields


class AvailabilityConditionSchema(BaseSchema):
    version = fields.Str()
    id = fields.Str()
    FromDate = fields.AwareDateTime()
    ToDate = fields.AwareDateTime()


class ServiceCalendarSchema(BaseSchema):
    id = fields.Str()
    FromDate = fields.Date("%Y-%m-%d")
    ToDate = fields.Date("%Y-%m-%d")


class HolidaysContentSchema(BaseSchema):
    ServiceCalendar = fields.Nested(ServiceCalendarSchema)
    AvailabilityConditions = fields.List(fields.Nested(AvailabilityConditionSchema))


class HolidaysResponseSchema(BaseSchema):
    Content = fields.Nested(HolidaysContentSchema)
