from types import SimpleNamespace

from marshmallow import Schema, fields, post_load
import yaml
from dotwiz import DotWiz

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

    def populate_defaults(self, screen, defaults):
        defaults.update(screen)
        return defaults

    @post_load
    def finalize(self, config, **kwargs):
        defaults = config.get("defaults")
        if defaults:
            for key, screens_list in config["screens"].items():
                for index, screen in enumerate(screens_list):
                    config["screens"][key][index] = self.populate_defaults(screen, defaults)
        return DotWiz(config)
