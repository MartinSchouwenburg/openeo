from flask_restful import Resource
from flask import request, Response
from globals import globalsSingleton
from userinfo import UserInfo
import os

class OpenEODownloadFile(Resource):
    def get(self, filepath):
        request_json = request.get_json()
        user = UserInfo(request)
        loc = globalsSingleton.openeoip_config['data_locations']
        root = loc['root_user_data_location']
        fullpath = os.path.join(root, user.username)       
        with open(fullpath, 'rb') as file:
            binary_data = file.read()
            response = Response(binary_data,
                            mimetype="application/octet-stream",
                            direct_passthrough=True)
            return response