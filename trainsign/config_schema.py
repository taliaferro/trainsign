from types import SimpleNamespace

from marshmallow import Schema, fields, post_load
import yaml
from dotwiz import DotWiz

class SerialDeviceConfigSchema(Schema):
    port = fields.String()      # /dev/ttyS0
    baudrate = fields.Integer() # 9600
    parity = fields.String()    # PARITY_EVEN
    bytesize = fields.String()  # EIGHTBITS 

class ScreenConfigSchema(Schema):
    display = fields.String()
    seconds = fields.Float()
    operator = fields.String()
    line = fields.String()
    stop = fields.String()

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

