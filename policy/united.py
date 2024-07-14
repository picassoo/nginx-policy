import os
import shutil

def printAllSubDirAndFile(path):
    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for subdirname in dirnames:
            print("Directory    :%s" % os.path.join(dirname, subdirname))

        for filename in filenames:
            print("File         :%s" % os.path.join(dirname, filename))    

def coreMoveToOutput(inputDirectory,outputDirectory):
    directories = [    f for f in os.listdir(inputDirectory) if os.path.isdir(os.path.join(inputDirectory, f)) ]

    nginxDir("conf.d",directories,inputDirectory,outputDirectory)        
    nginxDir("location.d",directories,inputDirectory,outputDirectory)        
    nginxDir("js.d",directories,inputDirectory,outputDirectory)        
    nginxDir("upstream.d",directories,inputDirectory,outputDirectory) 
    
    src = inputDirectory + "/nginx.conf"
    dst = outputDirectory + "/nginx.conf"
    shutil.copyfile(src, dst)


def appMoveToOutput(inputDirectory,outputDirectory):
    directories = [    f for f in os.listdir(inputDirectory) if os.path.isdir(os.path.join(inputDirectory, f)) ]

    nginxDir("location.d",directories,inputDirectory,outputDirectory)        
    nginxDir("upstream.d",directories,inputDirectory,outputDirectory) 


def nginxDir(ngxDir,dirnames,inputDirectory,outputDirectory):

    if ngxDir in dirnames:
        src = inputDirectory + "/" + ngxDir
        dst = outputDirectory + "/" + ngxDir
            
        createDirIfNotExists(dst)
        copyFiles(src,dst)  

def copyFiles(src,dest):

    files = [    f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f)) ]
    for file in files:
        inputFile = src+"/"+file
        outputFile = dest+"/"+file
        shutil.copyfile(inputFile, outputFile)

def createDirIfNotExists(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        print("Folder %s already exists" % path)

def uploadCertificates(inputDirectory,outputDirectory):
        src = inputDirectory + "/cert" 
        dst = outputDirectory + "/cert"

        createDirIfNotExists(dst)
        copyFiles(src,dst) 

if __name__ == "__main__":

    inputDirectory = "D:/Develop/PYTHON/nginx-policy/nginx-conf-demo"
    outputDirectory = "D:/Develop/PYTHON/nginx-policy/nginx-conf-demo-output"

    printAllSubDirAndFile(inputDirectory)
    
    print("---------------")

    createDirIfNotExists(outputDirectory)

    for i in os.listdir(inputDirectory):
        inputDir = os.path.join(inputDirectory, i)
        if i.__eq__("core"):
            coreMoveToOutput(inputDir,outputDirectory)
        else:
            appMoveToOutput(inputDir,outputDirectory)
    
    
    certDirectory = "D:/Develop/PYTHON/nginx-policy"
    uploadCertificates(certDirectory,outputDirectory)