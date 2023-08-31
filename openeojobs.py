from flask import make_response, jsonify, request
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager, makeBaseResponseDict
from userinfo import UserInfo
from constants.constants import *
from globals import globalsSingleton
from constants import constants

class OpenEOIPJobs(Resource):
    def processPostJobId(self, user, request_json):
        try:
            process = OpenEOProcess(user, request_json, 0)
            globalProcessManager.addProcess(process)
            url = request.base_url + "/" + process.job_id
            response =  make_response(jsonify(process.job_id),201)
            response.headers['OpenEO-Identifier'] = process.job_id
            response.headers['Location'] = url
            return response
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, 400, str(ex))
            return make_response(jsonify(err), err.code)   

    def processGetJobs(self, user): 
        try:        
            jobs = globalProcessManager.allJobsMetadata4User(user, None,request.base_url)
            return  make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, 400, str(ex))
            return make_response(jsonify(err), err.code) 
                      

    def post(self):
            request_json = request.get_json()
            user = UserInfo(request)
            return self.processPostJobId(user, request_json)
    def get(self):
            user = UserInfo(request)
            return self.processGetJobs(user)
          
class OpenEOJobResults(Resource):
   def returnJobResultUrls(self, job_id, user, request_json):
       return ""
       
   def queueJob(self, job_id, user, request_json):
        try:
            if not 'id' in request_json:
                err = globalsSingleton.errorJson(constants.CUSTOMERROR, job_id, 'missing \'job_id\' key in definition')
                return make_response(jsonify(err), err.code)
            
            message, error = globalProcessManager.queueJob(user, job_id)
            if error == "":
                return make_response(message, 202)
            else:
                err = globalsSingleton.errorJson(error, job_id, message)
                return make_response(jsonify(err),err.code)
                
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, job_id, str(ex))
            return make_response(jsonify(err), err.code)      
       
   def post(self, job_id):
        request_json = request.get_json()
        user = UserInfo(request)
        return self.queueJob(user, job_id, user, request_json)  

   def get(self, job_id):
        request_json = request.get_json()
        user = UserInfo(request)
        return self.returnJobResultUrls(user, job_id, user, request_json)   

class OpenEOIJobByIdEstimate(Resource):
   def processGetEstimate(self, job_id, user):
        try:
            estimate = globalProcessManager.makeEstimate(user, job_id)
            costs = estimate[0][2]
            return make_response(jsonify(costs),200) 
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, job_id, str(ex))
            return make_response(jsonify(err), err.code)       
       
   def get(self, job_id):
        user = UserInfo(request)
        return self.processGetEstimate(job_id, user)
 
        
class OpenEOMetadata4JobById(Resource):
    def processGetJobId(self, user, job_id):
        try:
            jobs = globalProcessManager.allJobsMetadata4User(user, job_id,request.base_url)
            return make_response(jsonify(jobs),200)
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, job_id, str(ex))
            return make_response(jsonify(err), err.code)  
        
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
                
                return make_response(jsonify(res),204)
            if status == STATUSQUEUED:
                err = globalsSingleton.errorJson("JobLocked", job_id, str(ex))
                return make_response(jsonify(err), err.code)      
               
        except Exception as ex:
            err = globalsSingleton.errorJson(constants.CUSTOMERROR, job_id, str(ex))
            return make_response(jsonify(err), err.code)    


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
     

        

        
