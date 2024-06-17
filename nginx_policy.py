import crossplane
import json

necessaryDirectives = ['proxy_ssl_certificate','proxy_ssl_certificate_key','proxy_ssl_verify']

def checkServerDirective(serverJsonStr):

    json_object = jsonify(serverJsonStr)
    #prettify(serverJsonStr)

    for block in serverJsonStr['block']:
        if(block['directive'] == "location"):
            checkLocationDirective(block)


def checkLocationDirective(locationJsonObj):
    directives = []
    prettify(locationJsonObj)
    for block in locationJsonObj['block']:
        directives.append(block['directive'])
    
    print("Directives :")
    print(directives)

    print("Control Result :")
    i = 0 
    for directive in necessaryDirectives:
        if directive not in directives:
            i=i+1
            result = f'{i} {directive} is not exist in'
            print(result)

    
def checkUpstreamDirective(serverJsonObj):
    prettify(serverJsonObj)

def prettify(jsonStr):
    print("---------------")
    print(jsonify(jsonStr))

def jsonify(jsonStr):
    jsonObj = json.dumps(jsonStr,indent=2)
    return jsonObj

if __name__ == "__main__":

    payload = crossplane.parse('D:/Develop/PYTHON/nginx.conf')
    results = json.dumps(payload,indent=2)

    #print(results)  

    json_object = json.loads(results)

    ## check main conf file and included conf files
    for conf in json_object['config']:
        for directive in conf['parsed']:    
            if(directive['directive'] == "server"):
                checkServerDirective(directive)
            if(directive['directive'] == "location"):
                checkLocationDirective(directive)

