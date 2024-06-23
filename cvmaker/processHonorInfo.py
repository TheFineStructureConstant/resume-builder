from cvmaker.baseProcessor import baseProcessor

# container class for honor information
class honorInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('honorEntry')
        self.processors = {
            'name': self.genericProcessor,
            'inst': self.genericProcessor,
            'date': self.genericProcessor,
            'location': self.genericProcessor,
        }
        self.processData(data)
