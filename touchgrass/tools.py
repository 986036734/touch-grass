"""Free, keyless web tools: geocoding, sun times, weather."""
import requests

UA = {"User-Agent": "touch-grass-agent/0.1 (hacktoberfest-week1)"}
TIMEOUT = 15


def geocode(place: str) -> dict:
    """Place name -> {'lat': float, 'lon': float, 'name': str} via OpenStreetMap Nominatim."""
    r = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": place, "format": "json", "limit": 1},
        headers=UA, timeout=TIMEOUT,
    )
    r.raise_for_status()
    hits = r.json()
    if not hits:
        raise ValueError(f"place not found: {place!r}")
    h = hits[0]
    return {"lat": float(h["lat"]), "lon": float(h["lon"]), "name": h["display_name"]}


def sun_times(lat: float, lon: float, date: str = "today") -> dict:
    """Sunrise/sunset/golden-hour for a coordinate via sunrise-sunset.org."""
    r = requests.get(
        "https://api.sunrise-sunset.org/json",
        params={"lat": lat, "lng": lon, "date": date, "formatted": 0},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    d = r.json()
    if d.get("status") != "OK":
        raise ValueError(f"sun API error: {d}")
    res = d["results"]
    return {
        "sunrise_utc": res["sunrise"],
        "sunset_utc": res["sunset"],
        "golden_hour_end": res.get("golden_hour"),
        "day_length": res.get("day_length"),
    }


def weather(lat: float, lon: float) -> dict:
    """Current + next-12h weather via Open-Meteo (no key)."""
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "hourly": "temperature_2m,precipitation_probability,weather_code",
            "forecast_hours": 12, "timezone": "auto",
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    d = r.json()
    cur = d.get("current", {})
    return {
        "temp_c": cur.get("temperature_2m"),
        "weather_code": cur.get("weather_code"),
        "wind_kmh": cur.get("wind_speed_10m"),
        "hourly_precip_prob": (d.get("hourly", {}).get("precipitation_probability") or [])[:12],
    }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "geocode",
            "description": "Resolve a place name to latitude/longitude.",
            "parameters": {"type": "object",
                           "properties": {"place": {"type": "string"}},
                           "required": ["place"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sun_times",
            "description": "Get sunrise/sunset times (UTC ISO) for coordinates.",
            "parameters": {"type": "object",
                           "properties": {"lat": {"type": "number"},
                                          "lon": {"type": "number"}},
                           "required": ["lat", "lon"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Get current weather and 12h precipitation outlook for coordinates.",
            "parameters": {"type": "object",
                           "properties": {"lat": {"type": "number"},
                                          "lon": {"type": "number"}},
                           "required": ["lat", "lon"]},
        },
    },
]

_DISPATCH = {"geocode": geocode, "sun_times": sun_times, "weather": weather}


def call_tool(name: str, args: dict):
    fn = _DISPATCH.get(name)
    if not fn:
        return {"error": f"unknown tool {name}"}
    try:
        return fn(**args)
    except Exception as exc:  # noqa: BLE001 - surface tool errors to the model
        return {"error": str(exc)}
