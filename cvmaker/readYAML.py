import yaml

def splitPath(name, dir = '.'):
    dirName = None
    if '/' in name:
        temp = name.split('/')
        name = temp.pop(-1) 
        dirName = "/".join(temp)
        dirName = f'{dir}/{dirName}'

    return name, dirName


def readYAMLFile(fname, dir='.'):
    
    data = {} 

    # read YAML files recursively
    with open(f"{dir}/{fname}", 'r') as yamlFile:
        data.update(yaml.safe_load(yamlFile))
    
    # read sub files
    for key,val in data.items():
        if 'files' in val:
            for entry in val['files']: 
                data[key].update(readYAMLFile(*splitPath(entry,dir)))
            del data[key]['files']
            

    if 'files' in data:
        for entry in data['files']:
            data.update(readYAMLFile(*splitPath(entry,dir)))

    # return data
    return data


if __name__ == "__main__":
    data = readYAMLFile('resume.yaml')
    print(data)
    print(data['personal_info'])
    print(data.keys())
