from datetime import datetime

# Example of serializing time
def serialize_time(time_obj):
    if isinstance(time_obj, datetime.time):
        return time_obj.strftime("%H:%M:%S")  # Convert to a string in "HH:MM:SS" format
    return time_obj  # Return as is for other types