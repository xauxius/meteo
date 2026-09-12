from enum import StrEnum

class Col(StrEnum):
    TIME_UTC = "timeUtc"
    TIME_LOCAL = "timeLocal"
    AIR_TEMPERATURE = "airTemperature"
    FEELS_LIKE_TEMPERATURE = "feelsLikeTemperature"
    WIND_SPEED = "windSpeed"
    WIND_GUST = "windGust"
    WIND_DIRECTION = "windDirection"
    CLOUD_COVER = "cloudCover"
    SEA_LEVEL_PRESSURE = "seaLevelPressure"
    RELATIVE_HUMIDITY = "relativeHumidity"
    PRECIPITATION = "precipitation"
    SNOW_DEPTH = "snowDepth"
    CONDITION_CODE = "conditionCode"

LOCAL_TIMEZONE = "Europe/Vilnius"