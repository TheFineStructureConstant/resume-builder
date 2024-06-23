# define date table
dateTable = { 
    "1": 'Jan',
    "2": 'Feb',
    "3": 'Mar',
    "4": 'Apr',
    "5": 'May',
    "6": 'June',
    "7": 'July',
    "8": 'Aug',
    "9": 'Sept',
    "10":'Oct',
    "11":'Nov',
    "12":'Dec'
}

def dateLookUp(date):

    data = date.split('-')
    year = data[0]
    month = dateTable[data[1]]
    day = data[2] if len(data) == 3 else None

    if day is not None:
        return f"{month} {day}, {year}"

    return f"{month} {year}"


# check if use key exists and points to a valid entry in the data
def checkKey(data):

    key = list(data.keys())[0]

    if 'use' in data:
        key = data['use'] if data['use'] in data else key

    # return available use keys
    return key


# check if list of use keys exists and points to a valid entry in the data
def checkKeyList(data):

    keys = [list(data.keys())[0]]

    # check for use keys
    if 'use' in data: 

        # handle case when use keys is a list
        if isinstance(data['use'], list):
            tempKeys = []
            for key in data['use']:
                if key in data:
                    tempKeys.append(key)
            
            if len(tempKeys) > 0:
                keys = tempKeys 

        # handle case where use keys is not a list
        else:
            keys = [data['use'] if data['use'] in data else keys]

    # return available use keys
    return keys
