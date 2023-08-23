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

            if process.workflow != None:
                outputInfo = process.workflow.run(False)

                if outputInfo["status"]:
                    if outputInfo["datatype"] != DTRASTER:
                        res = makeBaseResponseDict(process.job_id, 'finished', 200, request.base_url,  "Process completed succesfully")
                        res["data"] = {
                                    "type" : self.makeType(outputInfo["datatype"]),
                                    "format" : outputInfo["format"],
                                    "value" : outputInfo["value"]
                                }
                        return make_response(jsonify(res),200)
                elif outputInfo["datatype"] == DTRASTER:
                    #dummy probably not yet correct but the this how post and images work
                    with open(outputInfo["value"], 'rb') as file:
                        binary_data = file.read()
                        return Response(binary_data,
                                        mimetype="image/tiff",
                                        direct_passthrough=True)
                    
                return make_response(makeBaseResponseDict(process.job_id, 'error', 404, None, outputInfo["value"]))
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))
        

    def makeType(self, tp):
        if ( tp == DTNUMBER):
            return "number"
        if ( tp == DTRASTER):
            return "raster"
        return "unknown"

                        
                        

                

