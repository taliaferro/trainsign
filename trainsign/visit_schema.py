from marshmallow import Schema, fields, post_load


# for some reason the coordinate values are sometimes the empty string
# and Marshmallow doesn't handle that well.
class Coordinate(fields.Float):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == "":
            value = 0.0
        return super()._deserialize(value, attr, data, **kwargs)


class LocationSchema(Schema):
    longitude = Coordinate(allow_none=True, data_key="Longitude")
    latitude = Coordinate(allow_none=True, data_key="Latitude")


# I don't know what the heck this field is supposed to be for,
# but it's in their data so it's in the schema.
class FrameSchema(Schema):
    data_frame_ref = fields.Date("%Y-%m-%d", data_key="DataFrameRef")
    dated_vehicle_journey_ref = fields.String(data_key="DatedVehicleJourneyRef")


class VehicleStatusSchema(Schema):
    stop_ref = fields.Integer(data_key="StopPointRef")
    stop_name = fields.String(data_key="StopPointName")
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
    stop_display = fields.String(data_key="DestinationDisplay")


class JourneySchema(Schema):
    line_ref = fields.String(data_key="LineRef")
    direction = fields.String(data_key="DirectionRef")
    frame = fields.Nested(FrameSchema, data_key="FramedVehicleJourneyRef")
    line_name = fields.String(data_key="PublishedLineName")
    operator = fields.String(data_key="OperatorRef")
    origin_ref = fields.Integer(data_key="OriginRef")
    origin_name = fields.String(data_key="OriginName")
    destination_ref = fields.Integer(data_key="DestinationRef")
    destination_name = fields.String(data_key="DestinationName")
    monitored = fields.Boolean(data_key="Monitored")
    in_congestion = fields.Boolean(allow_none=True, data_key="InCongestion")
    vehicle_location = fields.Nested(LocationSchema, data_key="VehicleLocation")
    bearing = fields.Float(allow_none=True, data_key="Bearing")
    occupancy = fields.String(allow_none=True, data_key="Occupancy")
    vehicle_ref = fields.Integer(allow_none=True, data_key="VehicleRef")
    status = fields.Nested(VehicleStatusSchema, data_key="MonitoredCall")


class VisitSchema(Schema):
    timestamp = fields.AwareDateTime(data_key="RecordedAtTime")
    ref = fields.String(data_key="MonitoringRef")
    journey = fields.Nested(JourneySchema, data_key="MonitoredVehicleJourney")

    @post_load
    def collapse(self, data, **kwargs):
        data.update(data["journey"])
        data.pop("journey")
        return data
