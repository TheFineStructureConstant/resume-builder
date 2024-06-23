from cvmaker.baseProcessor import baseProcessor

# container class for education information
class educationInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('educationEntry')
        self.processors = {
            'degree': self.genericProcessor,
            'school': self.genericProcessor,
            'location': self.genericProcessor,
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
            'end': self.dateProcessor,
            'specialization': self.genericProcessor,
            'major': self.majorProcessor,
        }

        self.processData(data)

    # process major study areas with the potential for a list of majors
    def majorProcessor(self, **kwargs):
        data = kwargs['value']
        key = kwargs['key']
        self.dataFields.append(key)
        majorInfo = data
    
        # enure information is a list for join
        if not isinstance(majorInfo, list):
            majorInfo = [majorInfo]
        
        # record major information
        self.__dict__[key] = " and ".join(majorInfo)
