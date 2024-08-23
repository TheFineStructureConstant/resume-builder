from cvmaker.baseProcessor import baseProcessor

# container class for volunteer information
class volunteerInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('volunteerEntry')

        self.kwds = [
            'name', 'org', 'location',
            'start', 'stop', 'highlights',
        ]

        self.processors = {
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
        }

        self.processData(data)
