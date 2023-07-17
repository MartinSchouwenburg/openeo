from flask import make_response, jsonify, request
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager, makeBaseResponseDict
from datetime import datetime
from userinfo import UserInfo
from constants.constants import *



class OpenEOIPJobs(Resource):
    def post(self):
        request_doc = request.get_json()
        user = UserInfo(request)
        try:
            process = OpenEOProcess(user, request_doc, 0)
            globalProcessManager.addProcess(process)
            res  = makeBaseResponseDict(str(process.job_id),'created', 200, request.base_url )
            return make_response(jsonify(res),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))


    def get(self):
        try:
            user = UserInfo(request)
            jobs = globalProcessManager.allJobs4User(user, None,request.base_url)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))
       
            
        
class OpenEOIJobById2(Resource):
   def post(self, job_id):
        try:
            request_doc = request.get_json()
            if not 'id' in request_doc:
                return make_response(makeBaseResponseDict(-1, 'error', 404, None, 'missing \'job_id\' key in definition'))
            
            user = UserInfo(request)
            message = globalProcessManager.queueJob(user, job_id)
            return make_response(makeBaseResponseDict(-1, 'queued', 200, None, message))
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex))) 
    
class OpenEOIJobByIdEstimate(Resource):
   def get(self, job_id):
        try:
            user = UserInfo(request)
            estimate = globalProcessManager.makeEstimate(user, job_id)
            costs = estimate[0][2]
            res = makeBaseResponseDict(job_id,request.base_url,'updated', 200 )
            res['estimated'] = costs
            return make_response(jsonify(res),estimate[1]) 
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex))) 
        
class OpenEOIJobById(Resource):
    def get(self, job_id):
        try:
            user = UserInfo(request)
            jobs = globalProcessManager.allJobs4User(user, job_id,request.base_url)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))

    def delete(self, job_id):
        try:
            user = UserInfo(request)
            globalProcessManager.stopJob(user, job_id)        
            res = makeBaseResponseDict(job_id,'canceled', 204,request.base_url,'job has been successfully deleted' )
            return make_response(jsonify(res),204) 
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))
    
    def patch(self, job_id):
        try:
            status = globalProcessManager.removedCreatedJob(job_id)
            if status == STATUSCREATED:
                request_doc = request.get_json()
                user = UserInfo(request)
                process = OpenEOProcess(user, request_doc, job_id)
                globalProcessManager.addProcess(process)
                res = makeBaseResponseDict(job_id,'updated', 204,request.base_url )
                
                return make_response(jsonify(res),200)
            if status == STATUSQUEUED:
                res = makeBaseResponseDict(job_id,'error', 400,request.base_url,"Batch job is locked due to a queued or running batch computation." )
                return make_response(jsonify(res),400) 
               
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))
     

        

        
