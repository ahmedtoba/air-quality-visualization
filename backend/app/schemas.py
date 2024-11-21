from marshmallow import Schema, fields

class AirQualitySchema(Schema):
    timestamp = fields.DateTime(required=True)
    co = fields.Float(required=True)
    benzene = fields.Float()
    nox = fields.Float()
    no2 = fields.Float()
