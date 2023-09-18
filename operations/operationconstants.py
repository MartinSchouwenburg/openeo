OPERATION_SCHEMA_NUMBER = {'type' : [ 'number', 'null']}
OPERATION_SCHEMA_STRING = {'type' : [ 'string', 'null']}
OPERATION_SCHEMA_COLLECTIONID = { "type": "string","subtype": "collection-id","pattern": "^[\\w\\-\\.~/]+$"}
OPERATION_SCHEMA_BOUNDINGBOX = {"title": "Bounding Box", 
                                "type": "object", 
                                "subtype": "bounding-box", 
                                "required": ["west","south","east","north"],
                                 "properties": {
                                    "west": {
                                        "description": "West (lower left corner, coordinate axis 1).",
                                        "type": "number"
                                    },
                                    "south": {
                                            "description": "South (lower left corner, coordinate axis 2).",
                                            "type": "number"
                                    },
                                    "east": {
                                        "description": "East (upper right corner, coordinate axis 1).",
                                        "type": "number"
                                    },
                                    "north": {
                                        "description": "North (upper right corner, coordinate axis 2).",
                                        "type": "number"
                                    },
                                    "base": {
                                        "description": "Base (optional, lower left corner, coordinate axis 3).",
                                        "type": [
                                            "number",
                                            "null"
                                        ],
                                        "default": 'null'
                                    },
                                    "height": {
                                        "description": "Height (optional, upper right corner, coordinate axis 3).",
                                        "type": [
                                            "number",
                                            "null"
                                        ],
                                        "default": 'null'
                                    },
                                    "crs": {
                                        "description": "Coordinate reference system of the extent, specified as as [EPSG code](http://www.epsg-registry.org/) or [WKT2 CRS string](http://docs.opengeospatial.org/is/18-010r7/18-010r7.html). Defaults to `4326` (EPSG code 4326) unless the client explicitly requests a different coordinate reference system.",
                                        "anyOf": [
                                            {
                                                "title": "EPSG Code",
                                                "type": "integer",
                                                "subtype": "epsg-code",
                                                "minimum": 1000,
                                                "examples": [
                                                    3857
                                                ]
                                            },
                                            {
                                                "title": "WKT2",
                                                "type": "string",
                                                "subtype": "wkt2-definition"
                                            }
                                        ],
                                        "default": 4326
                                    }
                                } 
                            }
                               
                                
OPERATION_SCHEMA_TEMPORALEXTENT =  {
                    "type": "array",
                    "subtype": "temporal-interval",
                    "uniqueItems": 'true',
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "date-time",
                                "subtype": "date-time",
                                "description": "Date and time with a time zone."
                            },
                            {
                                "type": "string",
                                "format": "date",
                                "subtype": "date",
                                "description": "Date only, formatted as `YYYY-MM-DD`. The time zone is UTC. Missing time components are all 0."
                            },
                            {
                                "type": "null"
                            }
                        ]
                    },
                    "examples": [
                        [
                            "2015-01-01T00:00:00Z",
                            "2016-01-01T00:00:00Z"
                        ],
                        [
                            "2015-01-01",
                            "2016-01-01"
                        ]
                    ]
                }

OPERATION_SCHEMA_DATACUBE = {"type": "object","subtype": "datacube"}