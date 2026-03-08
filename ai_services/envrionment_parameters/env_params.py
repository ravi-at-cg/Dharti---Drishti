import requests
import math
from datetime import datetime
from collections import defaultdict
import statistics

# ------------------------------
# CONFIG
# ------------------------------


NASA_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# ------------------------------
# NASA POWER - CLIMATE
# ------------------------------

def fetch_climate(lat, lon, start, end):
    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,RH2M,T2MDEW,PRECTOTCORR",
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": start,
        "end": end,
        "format": "JSON"
    }

    res = requests.get(NASA_URL, params=params)
    res.raise_for_status()

    return res.json()["properties"]["parameter"]

# ------------------------------
# RAIN PATTERN ANALYSIS
# ------------------------------

def analyze_rain(rain_data):
    monthly = defaultdict(float)
    daily_values = []
    rainy_days = 0

    for date_str, value in rain_data.items():
        dt = datetime.strptime(date_str, "%Y%m%d")
        monthly[dt.month] += value
        daily_values.append(value)

        if value > 2:
            rainy_days += 1

    total_rain = sum(rain_data.values())
    avg_month = total_rain / 12
    peak_month = max(monthly, key=monthly.get)
    
    # Calculate daily and monthly averages
    avg_daily = statistics.mean(daily_values) if daily_values else 0
    
    # Month names
    month_names = ["", "January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    pattern = "distributed"
    if monthly[peak_month] > 2 * avg_month:
        pattern = "monsoon_dominant"

    return {
        "daily_mm": round(avg_daily, 2),
        "monthly_mm": round(avg_month, 2),
        "annual_mm": round(total_rain, 2),
        "rain_pattern": pattern,
        "rainy_days_count": rainy_days,
        "peak_rain_month": month_names[peak_month]
    }

# ------------------------------
# WEEKLY TEMPERATURE
# ------------------------------

def weekly_temperature(temp_data):
    weekly = defaultdict(list)

    for date_str, value in temp_data.items():
        dt = datetime.strptime(date_str, "%Y%m%d")
        week_num = int(dt.strftime('%U'))
        weekly[week_num].append(value)

    result = {}
    for week_num in sorted(weekly.keys())[:4]:  # First 4 weeks
        result[f"week_{week_num + 1}"] = round(statistics.mean(weekly[week_num]), 2)

    return result

# ------------------------------
# ELEVATION + SLOPE + ASPECT
# ------------------------------

def get_elevation(lat, lon):
    params = {"locations": f"{lat},{lon}"}
    res = requests.get(ELEVATION_URL, params=params)
    res.raise_for_status()

    return res.json()["results"][0]["elevation"]

def meters_per_degree_lat():
    return 111320

def meters_per_degree_lon(lat):
    return 111320 * math.cos(math.radians(lat))

def get_aspect_direction(aspect_deg):
    """Convert aspect degrees to cardinal direction"""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(aspect_deg / 45) % 8
    return directions[index]

def calculate_slope_aspect(lat, lon, delta=0.0005):
    z = get_elevation(lat, lon)
    z_north = get_elevation(lat + delta, lon)
    z_east = get_elevation(lat, lon + delta)

    dy = delta * meters_per_degree_lat()
    dx = delta * meters_per_degree_lon(lat)

    dz_dy = (z_north - z) / dy
    dz_dx = (z_east - z) / dx

    slope_rad = math.atan(math.sqrt(dz_dx**2 + dz_dy**2))
    slope_deg = math.degrees(slope_rad)
    slope_percent = math.tan(slope_rad) * 100

    aspect_rad = math.atan2(dz_dy, -dz_dx)
    aspect_deg = math.degrees(aspect_rad)

    if aspect_deg < 0:
        aspect_deg += 360

    return {
        "elevation_m": z,
        "slope_degree": round(slope_deg, 2),
        "slope_percent": round(slope_percent, 2),
        "aspect_degree": round(aspect_deg, 2),
        "aspect_direction": get_aspect_direction(aspect_deg)
    }

# ------------------------------
# WATERBODY DETECTION
# ------------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def check_waterbody(lat, lon, radius=1000):
    query = f"""
    [out:json];
    (
      way["natural"="water"](around:{radius},{lat},{lon});
      way["waterway"](around:{radius},{lat},{lon});
    );
    out center tags;
    """

    res = requests.post(OVERPASS_URL, data=query)
    
    # Check if response is valid before parsing JSON
    if not res.ok or not res.text.strip():
        return {
            "near_waterbody": "false",
            "distance_to_waterbody_m": None,
            "waterbody_type": None
        }
    
    try:
        data = res.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "near_waterbody": "false",
            "distance_to_waterbody_m": None,
            "waterbody_type": None
        }

    if not data["elements"]:
        return {
            "near_waterbody": "false",
            "distance_to_waterbody_m": None,
            "waterbody_type": None
        }

    closest = float("inf")
    closest_type = "unknown"
    
    for el in data["elements"]:
        if "center" in el:
            w_lat = el["center"]["lat"]
            w_lon = el["center"]["lon"]
        else:
            continue

        dist = haversine(lat, lon, w_lat, w_lon)
        if dist < closest:
            closest = dist
            # Determine waterbody type
            tags = el.get("tags", {})
            if "waterway" in tags:
                closest_type = tags["waterway"]
            elif "water" in tags:
                closest_type = tags["water"]
            else:
                closest_type = "water"

    return {
        "near_waterbody": "true",
        "distance_to_waterbody_m": round(closest, 2),
        "waterbody_type": closest_type
    }

# ------------------------------
# MASTER FUNCTION
# ------------------------------

def build_land_profile(lat, lon, start="20230101", end="20231231"):
    climate = fetch_climate(lat, lon, start, end)

    # Extract temperature data
    temp_values = list(climate["T2M"].values())
    temp_max_values = list(climate["T2M_MAX"].values())
    temp_min_values = list(climate["T2M_MIN"].values())
    humidity_values = list(climate["RH2M"].values())
    dew_point_values = list(climate["T2MDEW"].values())
    
    # Calculate averages
    avg_temp = round(statistics.mean(temp_values), 2)
    max_temp = round(max(temp_max_values), 2)
    min_temp = round(min(temp_min_values), 2)
    avg_humidity = round(statistics.mean(humidity_values), 2)
    avg_dew_point = round(statistics.mean(dew_point_values), 2)
    
    # Get rainfall analysis
    rainfall = analyze_rain(climate["PRECTOTCORR"])
    
    # Get weekly temperature averages
    weekly_temp = weekly_temperature(climate["T2M"])
    
    # Get terrain data
    terrain = calculate_slope_aspect(lat, lon)
    
    # Get waterbody data
    hydrology = check_waterbody(lat, lon)

    return {
        "terrain": terrain,
        "hydrology": hydrology,
        "climate": {
            "avg_temperature_c": avg_temp,
            "max_temperature_c": max_temp,
            "min_temperature_c": min_temp,
            "weekly_temp_averages_c": weekly_temp,
            "relative_humidity_percent": avg_humidity,
            "dew_point_c": avg_dew_point,
            "rainfall": {
                "daily_mm": rainfall["daily_mm"],
                "monthly_mm": rainfall["monthly_mm"],
                "annual_mm": rainfall["annual_mm"]
            },
            "rain_pattern": rainfall["rain_pattern"],
            "rainy_days_count": rainfall["rainy_days_count"],
            "peak_rain_month": rainfall["peak_rain_month"]
        }
    }


# ------------------------------
# RUN
# ------------------------------

if __name__ == "__main__":
    lat = 16.5062
    lon = 80.6480

    profile = build_land_profile(lat, lon)
    print(profile)