from cvmaker.baseProcessor import baseProcessor

# container class for honor information
class honorInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('honorEntry')
        
        self.kwds = [
            'name', 'inst', 'date', 'location',
        ]
        
        self.processData(data)
