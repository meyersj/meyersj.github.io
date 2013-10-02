import exifread, os, glob, datetime, ast, json

photos = glob.glob('/home/jeff/web/gitpage/trip/test_photos/*.jpeg')

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

  try:
    DateTime = datetime.datetime.strptime(str(tags[DateTime_tag]), "%Y:%m:%d %H:%M:%S")
    lat = coordinate_extract(str(tags[lat_tag]))
    lon = coordinate_extract(str(tags[lon_tag]))
    lat_ref = str(tags[lat_ref_tag])
    lon_ref = str(tags[lon_ref_tag])
    print photo_name
    
    if(lon_ref == 'W'):
      lon = -lon
    if(lat_ref == 'S'):
      kat = -lat

    data['lat'] = lat
    data['lon'] = lon
    data['datetime'] = DateTime      
    data['photo_name'] = photo_name
    dates.append(DateTime)

    f.close()
    photos_dict[DateTime] = data
  
  except KeyError:
    pass
  
dates.sort()


data_out = {'type': 'FeatureCollection','features': []}

count = 1

for date in dates:
  data = photos_dict[date]
  popupContent = "<img src=" + "test_photos/" + data['photo_name'] + "/>"
  feature_out = {'type':'Feature', 
                 'geometry':{'type':'Point', 
                 'coordinates':[data['lon'] , data['lat']]},
                 'properties':{'photo_name': data['photo_name'],
                               'count':count,
                               'popupContent':popupContent,
                               'datetime':str(data['datetime'])}}
                
  data_out['features'].append(feature_out)
  count += 1

f = open('test.geojson', 'w')
f.write(json.dumps(data_out, indent=2, separators=(',',': ')))
f.close()





