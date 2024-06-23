import jinja2
import os
from pathlib import Path

from cvmaker.processEduInfo import educationInfo
from cvmaker.processExpInfo import experienceInfo 
from cvmaker.processVolInfo import volunteerInfo 
from cvmaker.processTrainInfo import trainingInfo
from cvmaker.processHonorInfo import honorInfo
from cvmaker.processPresInfo import presentationInfo

# processor class for list information
class listInfoProcessor:
    def __init__(self, var, data):
        self.entries = []
        self.var = var
        self.secName = var.capitalize()
        self.currIndent = 0

        # check for other directives then grab data entires
        if isinstance(data, dict):
            if 'section_name' in data:
                self.secName = data['section_name'] 
            if 'entries' in data:
                data = data['entries']

        # define which yaml stanza maps to which processor
        self.entryProcessors = {
            'education': educationInfo, 
            'experience': experienceInfo, 
            'training': trainingInfo, 
            'volunteer': volunteerInfo, 
            'honors': honorInfo, 
            'presentation': presentationInfo, 
        }

        self.processor = self.entryProcessors[var]
        
        # setup jinja template stuff
        cwd = Path(os.path.dirname(os.path.realpath(__file__)))
        jinjaDir = cwd / "jinjaTemplates"
        self.jinjaEnv = jinja2.Environment(loader = jinja2.FileSystemLoader(jinjaDir))
        self.jinjaTemplate = self.jinjaEnv.get_template(f'env.tex.j2') 

        # extract entries
        self.processData(data)


    # process data into entries
    def processData(self, data):

        for entry in data:
            # check for use flags if available
            if 'use' in entry:
                if not entry['use']:
                    print(f"Skipping {self.var} entry")
                    continue
            
            # contstruct container for this entry if desired        
            self.entries.append(self.processor(entry))
            
    def setIndent(self, indent):
        self.currIndent = indent

    # return the length of this container
    def __len__(self):
        return len(self.entries)

    # add list type indexing
    def __getitem__(self, k):
        return self.entries[int(k)] 

    # render latex environment through jinja templates when converted to string
    def __str__(self): 
        return self.jinjaTemplate.render(
                 secName = self.secName,
                 envName = self.var,
                 entries = [str(entry) for entry in self.entries], 
                 currIndent = self.currIndent 
               ) 
