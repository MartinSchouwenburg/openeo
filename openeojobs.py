from flask import make_response, jsonify, request, Response
from flask_restful import Api, Resource
from workflow.openeoprocess import OpenEOProcess
from multiprocessing import Process

def runProcess(job):
    if job.workflow != None:
        outputInfo = job.workflow.run(False)


class OpenEOIPJobs(Resource):
    def post(self):
        request_doc = request.get_json()
        job = OpenEOProcess(request_doc)
        
