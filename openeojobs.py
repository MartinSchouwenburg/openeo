from flask import make_response, jsonify, request
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager, makeBaseResponseDict
from datetime import datetime
from userinfo import UserInfo
from constants.constants import *

class OpenEOIPJobs(Resource):
    def processPostJobId(self, user, request_json):
        try:
            process = OpenEOProcess(user, request_json, 0)
            globalProcessManager.addProcess(process)
            res  = makeBaseResponseDict(str(process.job_id),'created', 200, request.base_url )
            return make_response(jsonify(res),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))   

    def processGetJobs(self, user): 
        try:        
            jobs = globalProcessManager.allJobs4User(user, None,request.base_url)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex))) 
                      

    def post(self):
            request_json = request.get_json()
            user = UserInfo(request)
            return self.processPostJobId(user, request_json)
    def get(self):
            user = UserInfo(request)
            return self.processGetJobs(user)
          
class OpenEOIJobById2(Resource):
   def processPostJobIdResults(self, job_id, user, request_json):
        try:
            if not 'id' in request_json:
                return make_response(makeBaseResponseDict(-1, 'error', 404, None, 'missing \'job_id\' key in definition'))
            
            message = globalProcessManager.queueJob(user, job_id)
            return make_response(makeBaseResponseDict(-1, 'queued', 200, None, message))
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))        
       
   def post(self, job_id):
        request_json = request.get_json()
        user = UserInfo(request)
        return self.processPostJobIdResults(user, job_id, user, request_json)              

    
class OpenEOIJobByIdEstimate(Resource):
   def processGetEstimate(self, job_id, user):
        try:
            estimate = globalProcessManager.makeEstimate(user, job_id)
            costs = estimate[0][2]
            res = makeBaseResponseDict(job_id,request.base_url,'updated', 200 )
            res['estimated'] = costs
            return make_response(jsonify(res),estimate[1]) 
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))        
       
   def get(self, job_id):
        user = UserInfo(request)
        return self.processGetEstimate(job_id, user)
 
        
class OpenEOIJobById(Resource):
    def processGetJobId(self, user, job_id):
        try:
            jobs = globalProcessManager.allJobs4User(user, job_id,request.base_url)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))  
        
    def processDeleteId(self, job_id, user):
        try:
            globalProcessManager.stopJob(user, job_id)        
            res = makeBaseResponseDict(job_id,'canceled', 204,request.base_url,'job has been successfully deleted' )
            return make_response(jsonify(res),204) 
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))
        
    def processPatchId(self, job_id, user, request_json):
        try:
            status = globalProcessManager.removedCreatedJob(job_id)
            if status == STATUSCREATED:
                process = OpenEOProcess(user, request_json, job_id)
                globalProcessManager.addProcess(process)
                res = makeBaseResponseDict(job_id,'updated', 204,request.base_url )
                
                return make_response(jsonify(res),200)
            if status == STATUSQUEUED:
                res = makeBaseResponseDict(job_id,'error', 400,request.base_url,"Batch job is locked due to a queued or running batch computation." )
                return make_response(jsonify(res),400) 
               
        except Exception as ex:
            return make_response(makeBaseResponseDict(-1, 'error', 404, None, str(ex)))        


    def get(self, job_id):
        user = UserInfo(request)
        return self.processGetJobId(job_id, user)

    def delete(self, job_id):
        user = UserInfo(request)
        return self.processDeleteId(job_id, user)
    
    def patch(self, job_id):
        request_json = request.get_json()
        user = UserInfo(request)
        return self.processPatchId(job_id, user, request_json)
     

        

        
