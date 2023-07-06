from workflow.workflow import Workflow
from globals import getOperation
from constants.constants import *
import multiprocessing
from datetime import datetime
from constants.constants import *
import uuid


def get(key,values,  defaultValue):
    if key in values:
        return values[key]
    return defaultValue


class OpenEOParameter:
    def __init__(self, parm):
        self.schema = parm['schema']
        subt = self.schema['subtype']
        self.name = get('name', parm, '')
        self.description = get('description', parm, '')
        self.optional = get('optional', parm, False)
        self.deprecated = get('deprecated', parm, False)
        self.experimental = get('experimental', parm, False)
        self.default = get('default', parm, None)

        if subt == 'process-graph': 
            ret = parm['return']
            self.returnValue = (ret['description'], ret['schema'])
            self.parameters = [] 
            parms = parm['parameters']
            for parm in parms:
                self.parameters.append(OpenEOParameter(parm))

        if subt == 'datacube':
            dimensions = parm['dimensions']
            self.spatial_organization = []
            for dim in dimensions:
                tp = dim['type']
                if tp == 'spatial':
                    self.spatial_organization.append((tp, get('axis', dimensions, '')))
                if tp == 'geometry':
                    self.spatial_organization.append((tp, get('geometry', dimensions, '')))
                if tp in ['bands', 'temporal', 'other']:
                    self.spatial_organization.append(tp, tp)

    def toDict(self):
            parmDict = {}
            parmDict = self.schema
            parmDict['name'] = self.name
            parmDict['description'] = self.description
            parmDict['optional'] = self.optional
            parmDict['deprecated'] = self.deprecated
            parmDict['experimental'] = self.experimental
            if self.default != None:
                parmDict['default']  = self.default
            return parmDict                



class OpenEOProcess(multiprocessing.Process):
    def __init__(self, user, request_doc):
        if not 'process' in request_doc:
            raise Exception("missing \'process\' key returns definition")
        self.user = user
        processValues = request_doc['process']
        self.submitted = str(datetime.now())
        self.status = 'created'
        self.updated =  ''
        self.workflow = None
        self.id = get('id', processValues, '')
        self.title = get('title', processValues, '')
        self.summary = get('summary', processValues, '')
        self.description = get('description', processValues, '')
        self.job_id = uuid.uuid4() 
        self.workflow = Workflow(get('process_graph', processValues, None), getOperation)
        self.parameters = []
        if 'parameters' in processValues:
            for parameter in processValues['parameters']:
                self.parameters.append(OpenEOParameter(parameter))
        self.categories = get('categories', processValues, [])
        self.deprecated = get('deprecated', processValues, False)
        self.experimental = get('experimental', processValues, False)
        self.plan = get('plan', processValues, 'free')
        self.budget = get('budget', processValues, UNDEFNUMBER)
        self.log_level = get('log_level', processValues, 'All')

        self.exceptions = {}
        if "exceptions" in processValues:
            for ex in processValues['exceptions'].items():
                self.exceptions[ex[0]] = ex[1]        
                       
        self.returns = {}
        if 'returns' in processValues:
            returns = processValues['returns']

            self.returns['description'] = get('description', returns, '')
            
            if 'schema' in returns:
                self.returns['schema'] = returns['schema']
            else:
                raise Exception("missing \'schema\' key returns definition")
            
        self.examples = []
        if 'examples' in processValues:
            self.examples = get('examples', processValues, [])

        self.links = []
        if 'links' in processValues:
            self.links = get('links', processValues, [])            
            
    def setItem(self, key, dict):
        if hasattr(self, key):
            dict[key] = getattr(self, key)
        return dict

    def toDict(self, short=True):
        dictForm = {}
        dictForm['id'] = str(self.job_id)
        dictForm = self.setItem('title', dictForm)
        dictForm = self.setItem('description', dictForm)
        dictForm = self.setItem('deprecated', dictForm)
        dictForm = self.setItem('experimental', dictForm)
        dictForm = self.setItem('submitted', dictForm)
        dictForm = self.setItem('plan', dictForm)
        dictForm = self.setItem('budget', dictForm)
        if short == False:
            processDict = {}
            processDict = self.setItem('summary', processDict) 
            processDict = self.setItem('id', processDict) 
            processDict = self.setItem('desciption', processDict)
            parms = []
            for parm in self.parameters:
                parms.append(parm.toDict())
            if len(parms) > 0:
                processDict["parameters"] = parms

            processDict['returns'] = self.returns
            processDict['categories'] = self.categories
            if len(self.examples) > 0:
                processDict['examples'] = self.examples 
            if len(self.links) > 0:
                processDict['links'] = self.examples                 
            processDict['process_graph'] = self.workflow.sourceGraph
            dictForm['process'] = processDict
            dictForm['log_level'] = self.log_level

        return dictForm       

    def run(self, queue):
        if self.workflow != None:
            outputInfo = self.workflow.run(str(self.job_id), queue)

    
  
        