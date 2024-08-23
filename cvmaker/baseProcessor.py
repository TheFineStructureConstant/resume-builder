import jinja2
import os
import datetime
from pathlib import Path

from cvmaker.utils import dateLookUp 

# base text processing class
class baseProcessor:
    def __init__(self, templateName):
        self.dataFields = []
        self.processors = {}

        cwd = Path(os.path.dirname(os.path.realpath(__file__)))
        jinjaDir = cwd / "jinjaTemplates"
        self.jinjaEnv = jinja2.Environment(loader = jinja2.FileSystemLoader(jinjaDir))

        ext = 'bib' if 'bibtex' in templateName else 'tex'
        self.jinjaTemplate = self.jinjaEnv.get_template(f'{templateName}.{ext}.j2') 

    def keys(self):
        return self.dataFields

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self): 
        return self.jinjaTemplate.render(data = self)

    # process data
    def processData(self, data):
        for val in data.keys():
            if val not in self.kwds:
                continue

            procMethod = self.genericProcessor
            if val in self.processors.keys():
                procMethod = self.processors[val]

            procMethod(value = data[val], key = val)

    # basic processor to be shared across the specialized processors
    def genericProcessor(self, **kwargs):
        key = kwargs['key']
        self.dataFields.append(key)
        self.__dict__[key] = kwargs['value'] 

    # date processor 
    def dateProcessor(self, **kwargs):
        dateData = str(kwargs['value'])
        key = kwargs['key']
        self.dataFields.append(key)

        self.__dict__[key] = dateLookUp(dateData) if 'Present' not in dateData else 'Present'
