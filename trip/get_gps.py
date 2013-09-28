import exifread, os, glob, csv, datetime

photos = glob.glob('/home/jeff/web/bike_trip_photos/*.jpeg')

lat_tag = 'GPS GPSLatitude'
lon_tag = 'GPS GPSLongitude'
time_tag = 'Image DateTime'

coordinates = []
no_coordinates = []

def coordinate_extract(string):
    string_list = string.replace(" ", "")[1:-1].split(",")
    degrees = string_list[0]
    minutes = string_list[1].split("/")
    dec_minutes = float(minutes[0]) / float(minutes[1]) / 60
    coordinate = float(degrees) + dec_minutes
    #print string
    #print lat
    return coordinate


dates = []
photos = {}
for photo in photos:
  f = open(photo, 'rb')
  photo_name = os.path.basename(photo)
  tags = exifread.process_file(f)

  time_stamp = datetime.datetime.strptime(str(tags[time_tag]), "%Y:%m:%d %H:%M:%S")
  photos[time_stamp] = photo_name
  dates.append(time_stamp)
  
  try:
    lat = coordinate_extract(str(tags[lat_tag]))
    lon = coordinate_extract(str(tags[lon_tag]))
   

    print photo_name + " " + str(lat) + "-" + str(lon)
    #print lon
  except KeyError:
    x = 5
    #print "no coordinates"
    #no_coordinates.append(photo_name)

print dates
dates.sort()
print dates


