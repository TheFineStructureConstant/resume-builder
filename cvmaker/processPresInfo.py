from cvmaker.baseProcessor import baseProcessor

# container class for presentation information
class presentationInfo(baseProcessor):
    def __init__(self, data):
        super().__init__('presentationEntry')
        self.processors = {
            'meeting': self.genericProcessor,
            'inst': self.genericProcessor,
            'authors': self.authorProcessor,
            'location': self.genericProcessor,
            'date': self.dateProcessor,
            'title': self.genericProcessor,
            'description': self.genericProcessor,
        }
        
        self.processData(data)

    def authorProcessor(self, **kwargs):
        data = kwargs['value']
        key = kwargs['key']
        
        # record key data
        self.dataFields.append(key)

        # extract and format author data
        authorData = data

        if isinstance(authorData, list):
            temp = []
            for author in authorData:
                split = author.split(' ') 
                firstName = split[0]
                lastName = split[1]

                temp.append(f'{firstName[0]}. {lastName}')

            authorData = temp
        else:
            authorData = [data]

        self.__dict__[key] = ', '.join(authorData)
