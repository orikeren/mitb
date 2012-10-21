__author__ = 'orikeren'
from geolib import Location, GeoService
import datetime
from time import sleep

loc1 = Location(lat=32.0491, lng=34.8671, alt=0)
#loc2 = Location(lat=32.072, lng=34.8079)

#dist = GeoService.get_distance(loc1, loc2)

#new_location = GeoService.get_destination_location(loc1, 0.2, 30)
#new_lat = GeoService.get_destination_location2(loc1, 0.2, 30)



#print("original location is: %s" % repr(loc1))
#print("new location is: %s" % repr(new_location))
#print("new lat is: %f" % new_lat)


print repr(loc1)

angle = 45
bearing = 270
speed = 10

first_time = True
sleep_interval = 1000 / 1000
new_location = Location(0,0,0)
start_time = datetime.datetime.now()
while first_time or new_location.alt > 0:
    first_time = False
    current_time = datetime.datetime.now()
    td = current_time - start_time
    new_location = GeoService.get_object_current_location(loc1, angle, bearing, speed, td.total_seconds())
    print("object location after %f seconds: %s" % (td.total_seconds(),repr(new_location)))
    print("\n")
    sleep(sleep_interval)
