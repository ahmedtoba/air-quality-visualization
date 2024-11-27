from marshmallow import Schema, fields

class AirQualityDataResponseSchema(Schema):
    timestamp = fields.DateTime(required=True, description="Timestamp of the record")
    CO_GT = fields.Float(required=False, description="CO concentration (mg/m³)")
    PT08_S1_CO = fields.Float(required=False, description="PT08.S1 (CO)")
    NMHC_GT = fields.Float(required=False, description="NMHC concentration (μg/m³)")
    C6H6_GT = fields.Float(required=False, description="Benzene concentration (μg/m³)")
    PT08_S2_NMHC = fields.Float(required=False, description="PT08.S2 (NMHC)")
    NOx_GT = fields.Float(required=False, description="NOx concentration (μg/m³)")
    PT08_S3_NOx = fields.Float(required=False, description="PT08.S3 (NOx)")
    NO2_GT = fields.Float(required=False, description="NO2 concentration (μg/m³)")
    PT08_S4_NO2 = fields.Float(required=False, description="PT08.S4 (NO2)")
    PT08_S5_O3 = fields.Float(required=False, description="PT08.S5 (O3)")
    T = fields.Float(required=False, description="Temperature (°C)")
    RH = fields.Float(required=False, description="Relative Humidity (%)")
    AH = fields.Float(required=False, description="Absolute Humidity (g/m³)")

class AirQualityDataParameterResponseSchema(Schema):
    timestamp = fields.DateTime(description="Timestamp of the record")
    parameter = fields.String(description="Air quality parameter to filter by")
    value = fields.Float(description="Value of the parameter")

class AirQualityDataUploadSchema(Schema):
    file = fields.Raw(required=True, description="CSV file containing air quality data", type="file")

class AirQualityDataFilterSchema(Schema):
    start_date = fields.Date(required=True, description="Start date for the query (DD-MM-YYYY)", format="%d-%m-%Y")
    end_date = fields.Date(required=True, description="End date for the query (DD-MM-YYYY)", format="%d-%m-%Y")

class AirQualityDataParametersFilterSchema(Schema):
    start_date = fields.Date(required=True, description="Start date for the query (DD-MM-YYYY)", format="%d-%m-%Y")
    end_date = fields.Date(required=True, description="End date for the query (DD-MM-YYYY)", format="%d-%m-%Y")
    parameters = fields.List(fields.String(), required=True, description="List of air quality parameters to filter by")