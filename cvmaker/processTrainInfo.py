from cvmaker.baseProcessor import baseProcessor

# container class for training information
class trainingInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('trainingEntry')
        self.processors = {
            'name': self.genericProcessor,
            'inst': self.genericProcessor,
            'date': self.dateProcessor,
            'start': self.dateProcessor,
            'stop': self.dateProcessor,
            'location': self.locProcessor,
        }
        self.processData(data)

    def locProcessor(self, **kwargs):
        key = kwargs['key']
        data = kwargs['value']

        self.dataFields.append(key)

        if not isinstance(data, list):
            data = [data]

        self.__dict__[key] = ' / '.join(data)
