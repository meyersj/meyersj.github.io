import exifread, os, glob, csv, datetime

photos = glob.glob('/home/jeff/web/gitpage/trip/test_photos/*.jpeg')

output_file = open('output.csv', 'wb')
output_table = csv.writer(output_file)

lat_tag = 'GPS GPSLatitude'
lon_tag = 'GPS GPSLongitude'
DateTime_tag = 'Image DateTime'
lat_ref_tag = 'GPS GPSLatitudeRef'
lon_ref_tag = 'GPS GPSLongitudeRef'
orientation_tag = 'Image Orientation'

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
photos_dict = {}

for photo in photos:
  f = open(photo, 'rb')
  data = {}
  photo_name = os.path.basename(photo)
  tags = exifread.process_file(f)
  DateTime = datetime.datetime.strptime(str(tags[DateTime_tag]), "%Y:%m:%d %H:%M:%S")
  


  try:
    lat = coordinate_extract(str(tags[lat_tag]))
    lon = coordinate_extract(str(tags[lon_tag]))
    lat_ref = str(tags[lat_ref_tag])
    lon_ref = str(tags[lon_ref_tag])


    if(lon_ref == 'W'):
      lon = -lon
    if(lat_ref == 'S'):
      kat = -lat

    data['lat'] = lat
    data['lon'] = lon
    data['photo_name'] = photo_name
    data['datetime'] = DateTime      
    dates.append(DateTime)
    print photo_name
    print tags[orientation_tag]
  except KeyError:
    pass

  photos_dict[DateTime] = data

dates.sort()


count = 1
output_table.writerow(['photo_name', 'popupContent', 'datetime', 'count', 'lat', 'lon'])

for date in dates:
  data = photos_dict[date]
  output_table.writerow([ data['photo_name'], \
                          "<img src=" + "test_photos/" + data['photo_name'] + "/>", \
                          str(data['datetime']), str(count), \
                          data['lat'], data['lon'] ]) 

  count += 1

output_file.close()





