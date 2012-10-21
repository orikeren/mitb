__author__ = 'orikeren'

import math





class GeoService(object):
    """
    main service class
    """

    EARTH_KM_RADIUS = 6371.01
    EARTH_METER_RADIUS = EARTH_KM_RADIUS * 1000
    GRAVITY_FACTOR = 9.81


    @classmethod
    def get_distance(cls, loc1, loc2):
        """
        returns the distance in km between 2 locations w/o considering the altitude
        """
        lat_delta = math.radians(loc2.lat) - math.radians(loc1.lat)
        lng_delta = math.radians(loc2.lng) - math.radians(loc1.lng)

        rad_lat1 = math.radians(loc1.lat)
        rad_lat2 = math.radians(loc2.lat)

        a_factor = math.sin(lat_delta / 2) * math.sin(lat_delta / 2) \
            + math.sin(lng_delta / 2) * math.sin(lng_delta / 2) \
            * math.cos(rad_lat1) * math.cos(rad_lat2)

        c_factor = 2 * math.atan2(math.sqrt(a_factor), math.sqrt(1 - a_factor))
        return cls.EARTH_KM_RADIUS * c_factor

    @classmethod
    def get_destination_location(cls, origin, distance, bearing):
        """
        returns the destination location from a source point, distance and initial bearing
        the bearing is in angles (north=0) and it's only the initial one since the bearing moves
        as the earth is spiral
        """
        rad_bearing = math.radians(bearing)
        angular_distance = float(distance) / float(cls.EARTH_KM_RADIUS)

        lat_rad = math.asin(
            (math.sin(math.radians(origin.lat)) * math.cos(angular_distance))
            +
            (math.cos(math.radians(origin.lat)) * math.sin(angular_distance) * math.cos(rad_bearing))
        )

        lng_rad = math.radians(origin.lng) + math.atan2(
            math.sin(rad_bearing) * math.sin(angular_distance) * math.cos(math.radians(origin.lat)),
            math.cos(angular_distance) - math.sin(math.radians(origin.lat)) * math.sin(math.radians(lat_rad))
        )
        return Location(lat=math.degrees(lat_rad), lng=math.degrees(lng_rad))

    @classmethod
    def get_object_current_location(cls, origin, throwing_angle, initial_bearing, initial_velocity, time_passed):
        """
        returns the object's current location based on a set of parameters
        Args:
            origin: source location
            throwing_angle:   angle of the throw in relation to the ground in degrees
            initial_bearing:    the initial bearing (direction) in degrees
            initial_velocity:   initial throw speed in km/h
            time passed:    the time passed since the object started moving in seconds
        """

        #get the relevant flying time
        actual_time = min(time_passed, cls._get_object_flying_time(throwing_angle, initial_velocity))
        dist = cls._get_horizontal_distance(throwing_angle, initial_velocity, actual_time)
        dest_location = cls.get_destination_location(origin, dist, initial_bearing)
        dest_location.alt = cls._get_current_altitude(float(0), throwing_angle, initial_velocity, time_passed)
        return dest_location

    @classmethod
    def _kmhour_to_msec(cls, speed):
        """
        converts speed to meters / sec from km / hour
        """
        return speed / 3.6


    @classmethod
    def _get_object_flying_time(cls, throwing_angle, initial_velocity):
        """
        calculates the flying time in seconds for an object thrown in certain speed
        returns the value in seconds
        Args:
            throwing_angle: angle of the throw in relation to the ground in degrees
            initial_velocity:   initial throw speed in km/h
        """
        return 2 * cls._kmhour_to_msec(initial_velocity) * math.sin(math.radians(throwing_angle)) / cls.GRAVITY_FACTOR

    @classmethod
    def _get_horizontal_distance(cls, throwing_angle, initial_velocity, time_passed):
        """
        returns the distance traveled by an object on the horizontal axis in meters
        Args:
            throwing_angle:   angle of the throw in relation to the ground in degrees
            initial_velocity:   initial throw speed in km/h
            time passed:    the time passed since the object started moving in seconds
        """
        return cls._kmhour_to_msec(initial_velocity) * math.cos(math.radians(throwing_angle)) * time_passed

    @classmethod
    def _get_current_altitude(cls, initial_altitude, throwing_angle, initial_velocity, time_passed):
        """
        returns an object's current altitude in meters
        Args:
            throwing_angle:   angle of the throw in relation to the ground in degrees
            initial_velocity:   initial throw speed in km/h
            time passed:    the time passed since the object started moving in seconds
            initial_altitude:   the object's initial altitude
        """
        alt = initial_altitude + (cls._kmhour_to_msec(initial_velocity) * math.sin(math.radians(throwing_angle)) * time_passed) - (cls.GRAVITY_FACTOR * time_passed * time_passed / 2.0)
        return max(alt,0)

class Location(object):
    """
    represents a location on earth
    """

    def __init__(self, lat = None, lng = None, alt = 0):
        """
        simple c'tor for the location class
        """
        self.lng = lng
        self.lat = lat
        self.alt = alt

    def __repr__(self):
        """
        short format if no alt and long format
        """
        return "(%f, %f, alt: %f)" % (self.lat, self.lng, self.alt)

