from .base_schema import BaseSchema
from marshmallow import fields


class FramedVehicleJourneySchema(BaseSchema):
    DataFrameRef = fields.Date("%Y-%m-%d")
    DatedVehicleJourneyRef = fields.String()


class VehicleLocationSchema(BaseSchema):
    Longitude = fields.Float()
    Latitude = fields.Float()


class MonitoredCallSchema(BaseSchema):
    StopPointRef = fields.Integer()
    StopPointName = fields.String()
    VehicleLocationAtStop = fields.String()
    VehicleAtStop = fields.Boolean(truthy={"true"}, falsy={"false", ""})
    AimedArrivalTime = fields.AwareDateTime(allow_none=True)
    ExpectedArrivalTime = fields.AwareDateTime(allow_none=True)
    AimedDepartureTime = fields.AwareDateTime(allow_none=True)
    ExpectedDepartureTime = fields.AwareDateTime(allow_none=True)
    Distances = fields.String()


class MonitoredVehicleJourneySchema(BaseSchema):
    LineRef = fields.String()
    DirectionRef = fields.String()
    FramedVehicleJourneyRef = fields.Nested(FramedVehicleJourneySchema)
    PublishedLineName = fields.String()
    OperatorRef = fields.String()
    OriginRef = fields.Integer()
    OriginName = fields.String()
    DestinationRef = fields.Integer()
    DestinationName = fields.String()
    Monitored = fields.Boolean()
    InCongestion = fields.Boolean(allow_none=True)
    VehicleLocation = fields.Nested(VehicleLocationSchema)
    Bearing = fields.Float(allow_nan=True)
    Occupancy = fields.String()
    VehicleRef = fields.Integer(allow_none=True)
    MonitoredCall = fields.Nested(MonitoredCallSchema)


class MonitoredStopVisitSchema(BaseSchema):
    RecordedAtTime = fields.AwareDateTime()
    MonitoringRef = fields.String()
    MonitoredVehicleJourney = fields.Nested(MonitoredVehicleJourneySchema)


class StopMonitoringDeliverySchema(BaseSchema):
    version = fields.String()
    ResponseTimestamp = fields.AwareDateTime()
    Status = fields.Boolean()
    MonitoredStopVisit = fields.List(fields.Nested(MonitoredStopVisitSchema))


class ServiceDeliverySchema(BaseSchema):
    ResponseTimestamp = fields.AwareDateTime()
    ProducerRef = fields.String()
    Status = fields.Boolean()
    StopMonitoringDelivery = fields.Nested(StopMonitoringDeliverySchema)


class StopMonitoringResponseSchema(BaseSchema):
    ServiceDelivery = fields.Nested(ServiceDeliverySchema)
