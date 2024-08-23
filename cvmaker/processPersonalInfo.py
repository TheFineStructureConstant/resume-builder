from cvmaker.baseProcessor import baseProcessor
from cvmaker.utils import checkKey, checkKeyList 

# class to process personal information
class personalInfoProcessor(baseProcessor):
    def __init__(self, var, data):
        super().__init__(var)

        self.kwds = [
            'name', 'address', 'position', 
            'clearance', 'phone', 'email',
        ]

        self.processors = {
            'name': self.processName,
            'address': self.processAddress,
            'clearance': self.processClearance,
            'phone': self.processPhone,
            'email': self.processEmail,
        } 

        # create class variables for the given data
        self.processData(data)

    # process name data
    def processName(self, **kwargs):
        data = kwargs['value']
        for name in ['first','last']:
            if name in data:
                self.dataFields.append(f'{name}name') 
                self.__dict__[f'{name}name'] = data[name]

    # process Address data
    def processAddress(self, **kwargs):
        data = kwargs['value']
        
        # check for use indicator and use first entry if not
        key = checkKey(data) 

        # load data into class structure
        self.dataFields.append('address')
        self.address = data[key] 

    # process clearance info
    def processClearance(self, **kwargs):
        data = kwargs['value'] 
        # process caveats which may be in a list or not
        caveats = ""
        if 'caveats' in data:
            temp = data['caveats']
            if not isinstance(temp, list):
                temp = [temp]
            
            for caveat in temp:
                caveats += f"/{caveat}"

        self.dataFields.append('clearance')
        self.clearance = f"{data['agency']} {data['level']}{caveats} Clearance"
    
    # process phone information
    def processPhone(self, **kwargs):
        data = kwargs['value']
        
        # get use indicators otherwise use first entry
        keys = checkKeyList(data) 

        # process phone data for available keys
        for key in keys:
            self.dataFields.append(f'{key}phone')
            self.__dict__[f'{key}phone'] = data[key]

    def processEmail(self, **kwargs):
        data = kwargs['value']
        
        # get use key indicator
        key = checkKey(data)

        # extract email data
        self.dataFields.append('email')
        self.email = data[key]
