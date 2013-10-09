import exifread, os, glob, datetime, ast, json
from urlparse import urlparse
from os.path import basename

photos = glob.glob('/home/jeff/web/bike_trip_photos/test_photos/*.jpeg')

lat_tag = 'GPS GPSLatitude'
lon_tag = 'GPS GPSLongitude'
DateTime_tag = 'Image DateTime'
lat_ref_tag = 'GPS GPSLatitudeRef'
lon_ref_tag = 'GPS GPSLongitudeRef'
orientation_tag = 'Image Orientation'
width_tag = 'EXIF ExifImageWidth'
height_tag = 'EXIF ExifImageLength'
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


dropbox = {}
with open('dropbox_photos.txt', 'rb') as f:
    content = f.readlines()

for url in content:
  url = url.replace('\n', '')
  dropbox[basename(urlparse(url).path)] = url


dates = []
photos_data = {}

for photo in photos:
  
  f = open(photo, 'rb')
  data = {}
  photo_name = os.path.basename(photo)
  tags = exifread.process_file(f)
  DateTime = datetime.datetime.strptime(str(tags[DateTime_tag]), "%Y:%m:%d %H:%M:%S")
  print photo_name
  
  #for tag in tags.keys():
    #print tag
  print tags[width_tag]
  print tags[height_tag]

  try:
    lat = coordinate_extract(str(tags[lat_tag]))
    lon = coordinate_extract(str(tags[lon_tag]))
    lat_ref = str(tags[lat_ref_tag])
    lon_ref = str(tags[lon_ref_tag])
    
    if lon_ref == 'W':
      lon = -lon
    if lat_ref == 'S':
      lat = -lat

    f.close()
  except KeyError:
    lat = 45.5720
    lon = -123.0810

  if photo_name == 're_photo2.jpeg':
    lon = -122.67193436622618
    lat = 45.52080050107107
  elif photo_name == 're_photo4.jpeg':
    lon = -122.83976554870604
    lat = 45.50394073994564
  elif photo_name == 're_photo30.jpeg':
    lon = -123.55924129486083
    lat = 45.58195317216897
  elif photo_name == 're_photo41.jpeg':
    lon = -123.971,
    lat = 45.354166666666664

 
  data['datetime'] = DateTime      
  data['photo_name'] = photo_name
  data['lat'] = lat
  data['lon'] = lon
  dates.append(DateTime)
  photos_data[DateTime] = data

dates.sort()
data_out = {'type': 'FeatureCollection','features': []}

count = 1
for date in dates:
  data = photos_data[date]
  popupContent = "<img src='%s'/>" % dropbox[data['photo_name']]
  #popupContent = ""
  feature_out = {'type':'Feature', 
                 'geometry':{'type':'Point', 
                 'coordinates':[data['lon'] , data['lat']]},
                 'properties':{'photo_name': data['photo_name'],
                               'count':count,
                               'popupContent':popupContent,
                               'date':str(data['datetime'])}}
                
  data_out['features'].append(feature_out)
  count += 1

f = open('test.geojson', 'w')
f.write(json.dumps(data_out, indent=2, separators=(',',': ')))
f.close()





