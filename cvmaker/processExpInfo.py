from cvmaker.baseProcessor import baseProcessor

# container class for experience information
class experienceInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('experienceEntry')
        self.processors = {
            'inst': self.genericProcessor,
            'dept': self.genericProcessor, 
            'position': self.genericProcessor,
            'location': self.genericProcessor,
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
            'highlights': self.genericProcessor
        }

        self.processData(data)
