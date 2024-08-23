from cvmaker.baseProcessor import baseProcessor

class skillInfoProcessor(baseProcessor):
    def __init__(self, var, data):
        super().__init__('skills')
        self.currIndent = 0 

        self.kwds = [
            'section_name', 'entries',
        ]
        self.processors = {
            'entries': self.entryProcessor
        }

        self.processData(data)
        self.dataFields.remove('section_name')

    def entryProcessor(self, **kwargs):
        for key,value in kwargs['value'].items():

            # check for use flags
            if 'use' in value:
                if not value['use']:
                    continue

                # shuffle data 
                value = value['entries'] 

            # extract data
            self.dataFields.append(key)
            self.__dict__[key] = ', '.join(value)

    def setIndent(self, indent):
        self.currIndent = indent
