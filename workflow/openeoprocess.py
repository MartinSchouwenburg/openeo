from workflow.workflow import Worklflow
from globals import globalsSingleton
from constants.constants import *

def get(key,values,  default):
    if key in values:
        return values[key]
    return default

class Schema:
    def __init__(self, parm):
        self.subtype = get('subtype', parm, '')
        self.deprecated = get('deprecated', parm, False)
        self.schemaUrl = get('$schema', parm, 'http://json-schema.org/draft-07/schema#')
        self.id = get('$id', parm, 'unknown')
        self.type = get('type', parm, 'unknown')
        self.regex = get('pattern', parm, '')
        self.enum = get('enum', parm, [])
        self.minimumum = get('minimum', parm, UNDEFNUMBER )
        self.maximum = get('maximum', parm, UNDEFNUMBER )
        self.minItems = get('minItems', parm, UNDEFNUMBER )
        self.maxItems = get('maxItems', parm, UNDEFNUMBER )  
        self.items = get('items', parm, [])    

class OpenEOParameter:
    def __init__(self, parm):
        schema = parm['schema']
        subt = schema['subtype']
        self.schema = Schema(schema)
        self.name = get('name', parm, '')
        self.description = get('description', parm, '')
        self.optional = get('optional', parm, False)
        self.deprecated = get('deprecated', parm, False)
        self.experimental = get('experimental', parm, False)
        self.default = get('default', parm, None)

        if subt == 'process-graph': 
            ret = parm['return']
            self.returnValue = (ret['description'], Schema(ret['schema']))
            self.parameters = [] 
            parms = parm['parameters']
            for parm in parms:
                self.parameters.append(OpenEOParameter(parm))

        if subt == 'datacude':
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

class OpenEOProcess:
    def __init__(self, request_doc):
        processValues = request_doc['process']

        self.workflow = None
        self.id = get('id', processValues, '')
        self.summary = get('summary', processValues, '')
        self.description = get('description', processValues, '')
        self.workflow = Worklflow(get('process_graph', processValues, None))
        self.parameters = []
        dd = 'parameters' in processValues
        if 'parameters' in processValues:
            for parameter in processValues['parameters']:
                self.parameters.append(OpenEOParameter(parameter))
        self.returns = {}
        self.returns['description'] = get('description', processValues['returns'], '')
        self.returns['schema'] = Schema(processValues['returns']['schema'])
        self.categories = get('categories', processValues, [])
        self.deprecated = get('deprecated', processValues, False)
        self.experimental = get('experimental', processValues, False)
        self.exceptions = {}
        if "exceptions" in processValues:
            for ex in processValues['exceptions'].items():
                self.exceptions[ex[0]] = ex[1]


