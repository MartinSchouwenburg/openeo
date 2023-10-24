from flask_restful import Resource
from flask import make_response, jsonify, request, Response
from constants.constants import *
from workflow.openeoprocess import OpenEOProcess
from userinfo import UserInfo
from processmanager import makeBaseResponseDict
from io import BytesIO
from zipfile import ZipFile
import os
from werkzeug.wsgi import FileWrapper
import pathlib

def getMimeType(filename):
    try:
        ext = pathlib.Path(filename).suffix
        if ext == '.jpg':
            return "image/jpeg"
        elif ext == '.tif' or ext == '.tiff':
            return 'image/tiff'
        elif ext == '.png':
            return "image/png" 
        return 'application/octet-stream'
    except:
        return 'application/octet-stream'
          
        
class OpenEOIPResult(Resource):
    def post(self):
        request_json = request.get_json()
        user = UserInfo(request)
        try:
            process = OpenEOProcess(user, request_json,0)

            if process.processGraph != None:
                outputInfo = process.processGraph.run(process.job_id, None, None)

                if outputInfo["status"] == STATUSFINISHED:
                    if outputInfo["datatype"] == DTRASTER or outputInfo["datatype"] == DTRASTERLIST :
                        if len(outputInfo["value"]) ==1:
                            filename = outputInfo["value"][0]
                            mimet = getMimeType(filename)
                            with open(filename, 'rb') as file:
                                binary_data = file.read()
                                response = Response(binary_data,
                                                mimetype=mimet,
                                                direct_passthrough=True)
                        else:   
                            stream = BytesIO()
                            with ZipFile(stream, 'w') as zf:                                                         
                                for fn in outputInfo["value"]:
                                    zf.write(file, os.path.basename(file))
                                stream.seek(0)
                                w = FileWrapper(stream)
                                response = Response(w,
                                                mimetype="application/x-zip",
                                                direct_passthrough=True)

                          
                    elif outputInfo["datatype"] != DTRASTER:
                        response = Response(str(outputInfo["value"]), mimetype = "string", direct_passthrough=True)
                        response.headers['Content-Type'] = 'string'
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

                        
                        

                

