import shapefile
# pip install pyshp, shp파일 관련 모듈
import json

path = "/temp"
sf = shapefile.Reader(path)

fields = sf.fields[1:]
field_names = [field[0] for field in fields]

buffer = []
for sr in sf.shapeRecords():
   atr = dict(zip(field_names, sr.record))

   geom = sr.shape.__geo_interface__
   buffer.append(dict(type="Feature", geometry=geom, properties=atr))

geojson = open("pyshp-demo.geojson", "w")
geojson.write(json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2, ensure_ascii=False))
geojson.close()