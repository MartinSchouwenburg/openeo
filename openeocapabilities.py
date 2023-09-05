from flask_restful import Resource
from flask import make_response, jsonify, request
    
from globals import globalsSingleton

OPENEO_GIP_ROOT = "http://127.0.0.1:5000/"

CAPABILITIES = {
        "api_version": "1.2.0",
        "backend_version": "0.1-alpha1",
        "stac_version": "1.0.0",
        "type": "Catalog",
        "id": "openeo-itc-gip-driver",
        "title": "itc-gip Driver",
        "description": "ITC-GIP OpenEO driver",
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
                "path": "/udf_runtimes",
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
            {
                "path": "/jobs/{job_id}/estimate",
                "methods": [
                    "GET"
                ]
            },
            {
                "path": "/validation",
                "methods": [
                    "POST"
                ]
            }                                              
        ],
        "links": [
            {
                "href": OPENEO_GIP_ROOT,
                "rel": "about",
                "type": "text/html",
                "title": "Homepage of the service provider"
            },
            {
                "href": OPENEO_GIP_ROOT + "collections",
                "rel": "data",
                "type": "application/json",
                "title": "List of Datasets"
            }
            ]
    }  
   
class OpenEOIPCapabilities(Resource):
    def get(self):
        ##version = globalsSingleton.openeoip_config['version']
       
        return make_response(jsonify(CAPABILITIES), 200)
    

    # https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICE_TYPES = {}


class OpenEOIPServiceTypes(Resource):

    def get(self, ):
        return make_response(jsonify(SERVICE_TYPES), 200)


# https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICES = []

def replace_links_in_capabilities():
    new_url = request.root_url.rstrip('/')

    for i in CAPABILITIES['links']:
        sample_url = i['href']
        split_sample = sample_url.split('/')
        if sample_url.startswith('http'):
            sample_url = "%s//%s" % (split_sample[0], split_sample[2])
        else:
            sample_url = split_sample[0]
        i['href'] = i['href'].replace(sample_url, new_url)
    return CAPABILITIES

class OpenEOIPServices(Resource):

    def get(self, ):
        response = dict(services=SERVICES, links=[])
        return make_response(jsonify(response), 200)
    

   

