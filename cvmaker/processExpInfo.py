from cvmaker.baseProcessor import baseProcessor

# container class for experience information
class experienceInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('experienceEntry')
        
        self.kwds = [
            'inst', 'dept', 'position',
            'location', 'start', 'stop',
            'highlights',
        ]

        self.processors = {
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
        }

        self.processData(data)
