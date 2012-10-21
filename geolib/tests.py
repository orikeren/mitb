__author__ = 'orikeren'

from geolib import GeoService, Location

def simple_distance_test():
    """
    simple air distance test between 2 locations
    """
    rotchild12 = Location(32.06279, 34.77048)
    habima = Location(32.0721, 34.7790)
    dist = GeoService.get_distance(rotchild12, habima)
    meters_dist = int(dist * 1000)
    print(meters_dist)
    assert meters_dist == 1310

def destination_location_test():
    dist = 0.25

    rotchild12 = Location(32.06279, 34.77048)

    #we choose 0 as angle to cancel the angular distance
    dest = GeoService.get_destination_location(rotchild12, dist, 0)
    calc_dist = GeoService.get_distance(rotchild12, dest)
    assert int(dist * 1000) == int(calc_dist * 1000)