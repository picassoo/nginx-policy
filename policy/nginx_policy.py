import crossplane
from result import Result,Level 
import json

necessaryLocationDirectives = ['proxy_ssl_certificate','proxy_ssl_certificate_key','proxy_ssl_verify']
necessaryHttpHeaders= { 'X-XSS-Protection': ['0'], 'Strict-Transport-Security':[ 'max-age=63072000;', 'includeSubDomains;', 'preload']}

def checkServerDirective(serverJsonStr,path):

    for block in serverJsonStr['block']:
        if(block['directive'] == "location"):
            checkLocationDirective(block)


def checkLocationDirective(locationJsonObj,path):
    output = []
    
    directives = []
    #prettify(locationJsonObj)
    for block in locationJsonObj['block']:
        directives.append(block['directive'])
        if (block['directive'] == 'proxy_pass'):
            upstreamAdd = block['args'][0]
            if(startWithDollar(upstreamAdd) and (not startWithHttp(upstreamAdd)) ):
                result = f'{upstreamAdd} is upstream adress'
                output.append(Result(result,Level.INFO,path))
            elif((not startWithDollar(upstreamAdd)) and (not startWithHttp(upstreamAdd)) ):
                result = f' upstream adress doesn\'t start with http protocol or don\'t start any upstream definition : {upstreamAdd} '
                output.append(Result(result,Level.WARNING,path))

    for directive in necessaryLocationDirectives:
        if directive not in directives:
            result = f'{directive} is not exist in'
            output.append(Result(result,Level.ERROR,path))
            
        
    return output

def startWithDollar(upstream):
    return upstream.startswith('$') 
    
def startWithHttp(upstream):
    return (upstream.startswith('https://') or upstream.startswith('http://'))
    
def checkUpstreamDirective(serverJsonObj):
    prettify(serverJsonObj)

def prettify(jsonStr):
    print("---------------")
    print(jsonify(jsonStr))

def jsonify(jsonStr):
    jsonObj = json.dumps(jsonStr,indent=2)
    return jsonObj

if __name__ == "__main__":

    payload = crossplane.parse('D:/Develop/PYTHON/nginx-policy/nginx.conf')
    results = json.dumps(payload,indent=2)

    json_object = json.loads(results)

    ## check main conf file and included conf files

    for conf in json_object['config']:
        path = conf['file']
        for directive in conf['parsed']:    
            if(directive['directive'] == "server"):
                checkServerDirective(directive,path)

            if(directive['directive'] == "location"):
                output = checkLocationDirective(directive,path)
                for i in output:
                    j_data = json.dumps(i.__dict__,indent=4)
                    print(j_data)



