from flask_restful import Resource
from flask import make_response, jsonify, request
    
from globals import globalsSingleton

class OpenEOIPCapabilities(Resource):
    def get(self):
        version = globalsSingleton.openeoip_config['version']
        CAPABILITIES = {
            "api_version": "1.0.1",
            "backend_version": version,
            "stac_version": "0.9.0",
            "id": "openeo-ilwispy-driver",
            "title": "IlwisPy Driver",
            "description": "IlwisPy OpenEO driver",
            "endpoints": [
                {
                    "path": "/service_types",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/services",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/result",
                    "methods": [
                        "POST"
                    ]
                },
                {
                    "path": "/collections",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/collections/{collection_id}",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/processes",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/processes/{process_id}",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/file_formats",
                    "methods": [
                        "GET"
                    ]
                },
                {
                    "path": "/jobs",
                    "methods": [
                        "GET", "POST", "DELETE"
                    ]
                },
                {
                    "path": "/jobs/{job_id}",
                    "methods": [
                        "GET", "PATCH", "DELETE"
                    ]
                },
                {
                    "path": "/jobs/udf_runtimes",
                    "methods": [
                        "GET"
                    ]
                },        
                {
                    "path": "/jobs/{job_id}/results",
                    "methods": [
                        "GET", "POST", "DELETE"
                    ]
                },
            ],
            "links": [
                {
                    "href": "http://www.test-openeo-ip.org",
                    "rel": "about",
                    "type": "text/html",
                    "title": "Homepage of the service provider"
                },
                {
                    "href": "https://www.test-openeo-ip.org/tos",
                    "rel": "terms-of-service",
                    "type": "text/html",
                    "title": "Terms of Service"
                },
                {
                    "href": "https://www.test-openeo-ip.org/privacy",
                    "rel": "privacy-policy",
                    "type": "text/html",
                    "title": "Privacy Policy"
                },
                {
                    "href": "http://www.test-openeo-ip.org/.well-known/openeo",
                    "rel": "version-history",
                    "type": "application/json",
                    "title": "List of supported openEO versions"
                },
                {
                    "href": "http://www.test-openeo-ip.org/api/v1.0/collections",
                    "rel": "data",
                    "type": "application/json",
                    "title": "List of Datasets"
                }
                ]
        }        
        return make_response(jsonify(CAPABILITIES), 200)
    

    # https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICE_TYPES = {}


class OpenEOIPServiceTypes(Resource):

    def get(self, ):
        return make_response(jsonify(SERVICE_TYPES), 200)


# https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICES = []


class OpenEOIPServices(Resource):

    def get(self, ):
        response = dict(services=SERVICES, links=[])
        return make_response(jsonify(response), 200)
    

   

