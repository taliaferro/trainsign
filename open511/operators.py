from marshmallow import fields
from .base_schema import BaseSchema


class OperatorSchema(BaseSchema):
    id = fields.String(data_key="Id")
    name = fields.String(data_key="Name")
    short_name = fields.String(data_key="ShortName", allow_none=True)
    siri_operator_ref = fields.String(data_key="SiriOperatorRef", allow_none=True)
    time_zone = fields.String(data_key="TimeZone")
    default_language = fields.String(data_key="DefaultLanguage")
    contact_telephone_number = fields.String(
        data_key="ContactTelephoneNumber", allow_none=True
    )
    web_site = fields.URL(data_key="WebSite", allow_none=True)
    primary_mode = fields.String(data_key="PrimaryMode")
    private_code = fields.String(data_key="PrivateCode")
    monitored = fields.Boolean(data_key="Monitored")
    other_modes = fields.String(data_key="OtherModes")
