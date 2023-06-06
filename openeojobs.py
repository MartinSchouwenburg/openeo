from flask import make_response, jsonify, request
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager
from datetime import datetime



def runProcess(job):
    if job.workflow != None:
        outputInfo = job.workflow.run(False)


class OpenEOIPJobs(Resource):
    def post(self):
        request_doc = request.get_json()
        process = OpenEOProcess(request_doc)
        globalProcessManager.addProcess(process)

        res = { "job_id" : str(process.workflow.job_id),
                    "status" : "submitted",
                    "submitted" : str(datetime.now()),
                    "links" : {
                        "href" :  request.base_url + "/" + str(process.workflow.job_id),
                        "rel" : 'self',
                        "type" : "application/json"
                    }
                    }
        return make_response(jsonify(res),200)

        
