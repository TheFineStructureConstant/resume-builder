import os

from cvmaker.processPersonalInfo import personalInfoProcessor
from cvmaker.processListInfo import listInfoProcessor
from cvmaker.processSkillInfo import skillInfoProcessor
from cvmaker.processPubInfo import pubInfoProcessor 

class dataHandler:
    def __init__(self, data):
        self.availableData = data.keys() 
        self.foundKeys = []
        self.processors = {
            'personal_info': personalInfoProcessor,
            'education': listInfoProcessor,
            'experience': listInfoProcessor,
            'training': listInfoProcessor,
            'volunteer': listInfoProcessor,
            'honors': listInfoProcessor,
            'presentation': listInfoProcessor,
            'skills': skillInfoProcessor,
            'publications': pubInfoProcessor,
        }

        self.processData(data)

    # proces data from yaml file
    def processData(self, data):
        
        # create variable for each key in the dictionary 
        for var in self.availableData:
            if var not in self.processors: 
                continue
            self.foundKeys.append(var)
            self.__dict__[var] = self.processors[var](var, data[var]) 

    # generate key ordering
    def generateKeyOrder(self, ordering): 
        keyWriteOrder = self.foundKeys

        # check if the ordering is specified
        if ordering is not None:
            tempKeys = []
            missingKeys = []
            
            for key in ordering['order']:
                if key in self.foundKeys:
                    tempKeys.append(key)  
                else:
                    missingKeys.append(key)
                
            # check if missing keys is alright
            if len(missingKeys) > 0: 
                message = "The specified ordering has the following keys\n"
                message += "which are not available in the data provided:\n"
                for key in missingKeys:
                    message += f"  - {key}\n"
                message += "\n"
                message += "Would you like to continue?\n"
                message += "Enter [y/n]: "

                value = input(message)

                if value == 'n':
                    print("Exiting without generating data")
                    return -1 

            keyWriteOrder = tempKeys    

        
        keyWriteOrder.remove('personal_info')
        
        # return key ordering
        return keyWriteOrder
    
    # write to file
    def writeToFile(self, **kwargs):

        # extract keyword arguments
        fileName = kwargs['fileName'] 
        ordering = kwargs['ordering'] 
        build = kwargs['build'] 
        splitFiles = kwargs['splitFiles']

        # build set of available keys in the right order
        keyWriteOrder = self.generateKeyOrder(ordering)
        if keyWriteOrder == -1:
            return False 

        # write to file
        with open('resume.tex', 'w') as baseFile:

            # write header data
            firstPart  = "\\documentclass{article}\n"
            firstPart += "\n"
            firstPart += "\\usepackage{ForestResume}\n"
            firstPart += "\\pagestyle{fancy}\n\n"

            if self.publications:
                firstPart += "\\usepackage[giveninits=true,\n"
                firstPart += "             style=science,\n"
                firstPart += "             backend=biber,\n"
                firstPart += "             defernumbers=true,\n"
                firstPart += "             sorting=ydnt,\n"
                firstPart += "             sortcites=true]{biblatex}\n\n"
                firstPart += "\\renewcommand*{\\bibfont}{\\bodyfont\small}\n\n"


            # add personal info to first part
            firstPart += "% Define Personal Information\n"
            firstPart += f"{self.personal_info}\n"
            
            # get this show on the road
            firstPart += "\n\\begin{document}\n"

            baseFile.write(firstPart)

            # write data for each key to file
            for key in keyWriteOrder:

                keyFile = baseFile

                if splitFiles:
                    baseFile.write(f"\\input{{texFiles/{key}.tex}}\n")
                    if not os.path.exists("texFiles"):
                        os.mkdir("texFiles")
                    keyFile = open(f"texFiles/{key}.tex", "w")
                else:
                    self.__dict__[key].setIndent(1)

                keyFile.write(f"{self.__dict__[key]}")

                if splitFiles:
                    keyFile.close()

            # end document
            baseFile.write("\\end{document}\n")
        
        # write bibtex files
        if self.publications is not None:
            self.publications.writeBibDataToFile() 
        
        # return zero on success
        return True

# trash from early development 
if __name__ == "__main__":
    process = dataProcessor({'personal_info': 1})
# end trash
