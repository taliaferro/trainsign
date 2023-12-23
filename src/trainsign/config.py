import os

from marshmallow import Schema, fields, post_load
import yaml

def load_config(path: os.PathLike):
    with open(path, "r") as fh:
        raw_config = yaml.safe_load(fh)
    return ConfigSchema().load(raw_config)


class SerialDeviceConfigSchema(Schema):
    port = fields.String()  # /dev/ttyACM0
    baudrate = fields.Integer()  # 9600


class ScreenConfigSchema(Schema):
    display = fields.String()
    seconds = fields.Float()
    line = fields.String()
    stop = fields.String()
    direction = fields.String()


class ClientConfigSchema(Schema):
    url = fields.URL(default="https://api.511.org")
    api_key = fields.String(required=True)
    rate_limit = fields.Integer(default=60)
    rate_limit_overhead = fields.Integer(default=0)
    operators = fields.List(fields.String(required=True))


class ScreensListsSchema(Schema):
    init = fields.List(fields.Nested(ScreenConfigSchema()))
    loop = fields.List(fields.Nested(ScreenConfigSchema()))


class ConfigSchema(Schema):
    client = fields.Nested(ClientConfigSchema, required=True)
    defaults = fields.Nested(ScreenConfigSchema)
    screens = fields.Nested(ScreensListsSchema, required=True)
