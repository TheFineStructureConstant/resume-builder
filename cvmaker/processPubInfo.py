import jinja2
import os
from pathlib import Path

from cvmaker.baseProcessor import baseProcessor

class pubInfoEntry(baseProcessor):
    def __init__(self, data):
        super().__init__('bibtexEntry')
        
        print(f'In pubInfoEntry: {data}')
        self.processors = {
            'template': self.genericProcessor,
            'title': self.genericProcessor,
            'url': self.genericProcessor,
            'repnum': self.genericProcessor,
            'date': self.dateProcessor,
            'month': self.genericProcessor,
            'year': self.genericProcessor,
            'authors': self.authorProcessor,
            'keywords': self.keywordProcessor,
            'institution': self.genericProcessor,
            'notes': self.noteProcessor
        }

        self.processData(data)

    def __len__(self):
        return len(self.dataFields) 

    def listEntryProc(self, **kwargs):
        data = kwargs['value']
        key = kwargs['key']
        joinStr = kwargs['join']

        self.dataFields.append(key)
        authorInfo = data
    
        # enure information is a list for join
        if not isinstance(authorInfo, list):
            authorInfo = [authorInfo]
        
        # record author information
        self.__dict__[key] = joinStr.join(authorInfo)

    def keywordProcessor(self, **kwargs):
        self.listEntryProc(key = kwargs['key'], value = kwargs['value'], join = ' ; ') 
        self.dataFields.append('keyword')

    # process authors with the potential for a list
    def authorProcessor(self, **kwargs):
        self.listEntryProc(key = kwargs['key'], value = kwargs['value'], join = ' and ') 
        self.dataFields.append('author')

    def dateProcessor(self, **kwargs):
        data = kwargs['value']
        
        splitData = data.split('-')

        self.__dict__['year'] = splitData[0]
        self.__dict__['month'] = splitData[1]
        self.dataFields.append('month')
        self.dataFields.append('year')

    def noteProcessor(self, **kwargs):
        data = kwargs['value']

        for entry in data:
            if isinstance(entry, dict):
                for key in entry.keys():
                    if key.lower() == 'sponsor':
                        self.__dict__['sponsor'] = entry[key]
                        self.dataFields.append('sponsor')
                    
class pubInfoProcessor:
    def __init__(self, var, data):

        # create member variables
        self.data = {}
        self.currIndent = 0
        self.var = var
        self.secName = var.capitalize()

        if isinstance(data, dict):
            if 'section_name' in data:
                self.secName = data['section_name'] 
            if 'entries' in data:
                data = data['entries']

        # setup jinja template stuff
        cwd = Path(os.path.dirname(os.path.realpath(__file__)))
        jinjaDir = cwd / "jinjaTemplates"
        self.jinjaEnv = jinja2.Environment(loader = jinja2.FileSystemLoader(jinjaDir))
        self.jinjaTemplate = self.jinjaEnv.get_template(f'pubs.tex.j2') 

        # process data
        self.processData(data)
        self.setOffsets()
        
    # set counter offsets
    def setOffsets(self):
        
        # get number of entries per year
        numEntries = {}
        for key in self.data.keys():
            numEntries[key] = len(self.data[key])

        # sort the years in descending order
        numEntries = dict(sorted(numEntries.items(), reverse = True))

        # calculate offsets for each year
        self.bibOffsets = {}    
        for k in range(len(numEntries)-1, -1, -1):
            l = k-1
            count = 1
            while(l != -1):
                count += numEntries[list(numEntries.keys())[l]]
                l -= 1
                
            self.bibOffsets[list(numEntries.keys())[k]] = count 

    # process data
    def processData(self, data):
        for year in data.keys():

            self.data[year] = []
            for pubData in data[year]:
               self.data[year].append(pubInfoEntry(pubData))

    # write bib data to files
    def writeBibDataToFile(self):
        
        # create directory for the bibliographic files
        if not os.path.exists("bibFiles"):
            os.mkdir("bibFiles")

        # write data to file by year
        for year,data in self.data.items():
            with open(f"bibFiles/{year}.bib", "w") as bibTexFile:
                for entry in data:
                    bibTexFile.write(f"{entry}")

    # set indent for template output
    def setIndent(self, indent):
        self.currIndent = indent

    # render data as a string
    def __str__(self):
        print(self.currIndent)
        return self.jinjaTemplate.render(
                 secName = self.secName,
                 data = dict(sorted(self.data.items(), reverse = True)),
                 currIndent = self.currIndent,
                 offsets = self.bibOffsets
               ) 
