from .base_schema import BaseSchema
from marshmallow import fields


class Coordinate(fields.Float):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == "":
            value = 0.0
        return super()._deserialize(value, attr, data, **kwargs)


class VehicleLocationSchema(BaseSchema):
    longitude = Coordinate(allow_none=True, data_key="Longitude")
    latitude = Coordinate(allow_none=True, data_key="Latitude")


class FramedVehicleJourneySchema(BaseSchema):
    data_frame_ref = fields.Date("%Y-%m-%d", data_key="DataFrameRef")
    dated_vehicle_journey_ref = fields.String(data_key="DatedVehicleJourneyRef")


class MonitoredCallSchema(BaseSchema):
    stop_point_ref = fields.Integer(data_key="StopPointRef")
    stop_point_name = fields.String(data_key="StopPointName")
    vehicle_location_at_stop = fields.String(data_key="VehicleLocationAtStop")
    vehicle_at_stop = fields.Boolean(
        truthy={"true"}, falsy={"false", ""}, data_key="VehicleAtStop"
    )
    aimed_arrival_time = fields.AwareDateTime(
        allow_none=True, data_key="AimedArrivalTime"
    )
    expected_arrival_time = fields.AwareDateTime(
        allow_none=True, data_key="ExpectedArrivalTime"
    )
    aimed_departure_time = fields.AwareDateTime(
        allow_none=True, data_key="AimedDepartureTime"
    )
    expected_departure_time = fields.AwareDateTime(
        allow_none=True, data_key="ExpectedDepartureTime"
    )
    distances = fields.String(data_key="Distances")


class MonitoredVehicleJourneySchema(BaseSchema):
    line_ref = fields.String(data_key="LineRef")
    direction_ref = fields.String(data_key="DirectionRef")
    framed_vehicle_journey_ref = fields.Nested(
        FramedVehicleJourneySchema, data_key="FramedVehicleJourneyRef"
    )
    published_line_name = fields.String(data_key="PublishedLineName")
    operator_ref = fields.String(data_key="OperatorRef")
    origin_ref = fields.Integer(data_key="OriginRef")
    origin_name = fields.String(data_key="OriginName")
    destination_ref = fields.Integer(data_key="DestinationRef")
    destination_name = fields.String(data_key="DestinationName")
    monitored = fields.Boolean(data_key="Monitored")
    in_congestion = fields.Boolean(allow_none=True, data_key="InCongestion")
    vehicle_location = fields.Nested(VehicleLocationSchema, data_key="VehicleLocation")
    bearing = fields.Float(allow_none=True, data_key="Bearing")
    occupancy = fields.String(allow_none=True, data_key="Occupancy")
    vehicle_ref = fields.Integer(allow_none=True, data_key="VehicleRef")
    monitored_call = fields.Nested(MonitoredCallSchema, data_key="MonitoredCall")


class MonitoredStopVisitSchema(BaseSchema):
    recorded_at_time = fields.AwareDateTime(data_key="RecordedAtTime")
    monitoring_ref = fields.String(data_key="MonitoringRef")
    monitored_vehicle_journey = fields.Nested(
        MonitoredVehicleJourneySchema, data_key="MonitoredVehicleJourney"
    )


class StopMonitoringDeliverySchema(BaseSchema):
    version = fields.String(data_key="version")
    response_timestamp = fields.AwareDateTime(data_key="ResponseTimestamp")
    status = fields.Boolean(data_key="Status")
    monitored_stop_visit = fields.List(
        fields.Nested(MonitoredStopVisitSchema), data_key="MonitoredStopVisit"
    )


class ServiceDeliverySchema(BaseSchema):
    response_timestamp = fields.AwareDateTime(data_key="ResponseTimestamp")
    producer_ref = fields.String(data_key="ProducerRef")
    status = fields.Boolean(data_key="Status")
    stop_monitoring_delivery = fields.Nested(
        StopMonitoringDeliverySchema, data_key="StopMonitoringDelivery"
    )


class StopMonitoringResponseSchema(BaseSchema):
    service_delivery = fields.Nested(ServiceDeliverySchema, data_key="ServiceDelivery")
