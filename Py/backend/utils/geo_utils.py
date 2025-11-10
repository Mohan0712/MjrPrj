import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def nearest_hospitals(user_location, hospitals_list, top_n=5):
    """
    user_location: dict with 'latitude' and 'longitude'
    hospitals_list: list of dicts, each dict with 'latitude', 'longitude', 'name', etc.
    top_n: number of nearest hospitals to return
    """
    user_lat = user_location.get("latitude")
    user_lon = user_location.get("longitude")
    
    if user_lat is None or user_lon is None:
        return []

    # Calculate distances
    for hospital in hospitals_list:
        hosp_lat = hospital.get("latitude")
        hosp_lon = hospital.get("longitude")
        hospital["distance"] = haversine_distance(user_lat, user_lon, hosp_lat, hosp_lon)
    
    # Sort by distance
    nearest = sorted(hospitals_list, key=lambda x: x["distance"])[:top_n]
    return nearest
