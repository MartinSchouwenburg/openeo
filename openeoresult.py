from flask_restful import Resource
from flask import make_response, jsonify, request, Response
from constants.constants import *
from workflow.openeoprocess import OpenEOProcess
from userinfo import UserInfo
from processmanager import makeBaseResponseDict


class OpenEOIPResult(Resource):
    def post(self):
        request_json = request.get_json()
        user = UserInfo(request)
        try:
            process = OpenEOProcess(user, request_json,0)

            if process.processGraph != None:
                outputInfo = process.processGraph.run(process.job_id, None, None)

                if outputInfo["status"]:
                    if outputInfo["datatype"] != DTRASTER:
                        response = Response(str(outputInfo["value"]), mimetype = "string", direct_passthrough=True)
                        response.headers['Content-Type'] = 'string'
                        return response
                elif outputInfo["datatype"] == DTRASTER:
                    #dummy probably not yet correct but the this how post and images work
                    with open(outputInfo["value"], 'rb') as file:
                        binary_data = file.read()
                        response = Response(binary_data,
                                        mimetype="image/tiff",
                                        direct_passthrough=True)
                        return response
                    
                response =  make_response(makeBaseResponseDict(process.job_id, 'error', 404, None, outputInfo["value"]),400)
                response.headers['Content-Type'] = 'string'

                return response
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)),400)
        

    def makeType(self, tp):
        if ( tp == DTNUMBER):
            return "number"
        if ( tp == DTRASTER):
            return "raster"
        return "unknown"

                        
                        

                

