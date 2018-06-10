import os

def listAllFilesIn(myPath, extension):
    '''
    Returns a lists all of files in a given path with a given extension

    Dependencies: os
    '''
    filePaths = []
    for (dirpath, _, filenames) in os.walk(myPath):
        for filename in filenames:
            if filename.split('.')[-1] == extension:
                filePath = os.path.join(dirpath, filename)
                filePath = filePath.replace("\\", "/")  # only for windows
                filePaths.append(filePath)

    return filePaths