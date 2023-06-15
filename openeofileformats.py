from flask import Flask, jsonify
from flask_restful import Api, Resource

OUTPUT_FORMATS = {
  "output": {
    "GTiff": {
      "gis_data_types": [
        "raster"
      ],
      "parameters": {},
      "links": [{
        "href": "https://www.gdal.org/frmt_gtiff.html",
        "rel": "about",
        "title": "GDAL on the GeoTiff file format and storage options"
      }]
    }
  },
  "input": {}
}

class OpenEOIPFileFormats(Resource):
    def get(self):
        return jsonify(OUTPUT_FORMATS) 