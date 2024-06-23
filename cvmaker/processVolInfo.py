from cvmaker.baseProcessor import baseProcessor

# container class for volunteer information
class volunteerInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('volunteerEntry')
        self.processors = {
            'name': self.genericProcessor,
            'org': self.genericProcessor, 
            'location': self.genericProcessor,
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
            'highlights': self.genericProcessor
        }

        self.processData(data)
