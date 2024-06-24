from enum import Enum

class Result:

    def __init__(self,message,level,path) :
        self.message = message
        self.level = level
        self.path = path

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
    
class Level(str,Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Output:

    def __init__(self) :
        self.results= []

    def addResult(self,result):
        self.results.append(result)