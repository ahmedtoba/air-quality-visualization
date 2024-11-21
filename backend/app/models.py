class AirQuality:
    """Air quality document model."""
    collection_name = "air_quality"

    def __init__(self, timestamp, co, benzene, nox, no2):
        self.timestamp = timestamp
        self.co = co
        self.benzene = benzene
        self.nox = nox
        self.no2 = no2

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "co": self.co,
            "benzene": self.benzene,
            "nox": self.nox,
            "no2": self.no2,
        }
