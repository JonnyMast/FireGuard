from geopy.geocoders import Nominatim
from frcm.datamodel.model import Location


class LocationHelper:
    def city_to_coordinates(self, city: str):
        geolocator = Nominatim(user_agent="FireGuard")

        try:
            location = geolocator.geocode(city)
            if location:
                return Location(
                    latitude=location.latitude, longitude=location.longitude
                )
            else:
                return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None


location_helper = LocationHelper()
