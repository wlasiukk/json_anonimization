import sys
import random
import string
import json


def to_json(p_str:str) -> dict:
    try:
        a_json = json.loads(p_str)
        return a_json
    except:
        return None

def str_anonymize(p_input:str) ->str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=len(p_input)))

def int_anonymize(p_input:int) ->int:
    return int("".join(random.choices(string.digits, k=len(str(p_input)))))

def float_anonymize(p_input:float) ->float:
    str_input = str(p_input)
    spl = str_input.split(".")
    if len(spl)==2:
        return float( str(int_anonymize(spl[0]))+"."+str(int_anonymize(spl[1])) )
    elif len(spl)==1:
        return float( int_anonymize(spl[0]) )
    else:
        return float( int_anonymize( p_input ) )


def dict_anonymize(j:dict):
    for jk in j.keys():
        j[jk] = any_anonymize(j[jk])

def any_anonymize(p_any):
    if type(p_any)==str:
        if str(p_any).startswith(("{","[")):
            tmp_j = to_json(p_any)
            if tmp_j is not None:
                # looks like json in json - lets anonymize it :)
                dict_anonymize(tmp_j)
                return json.dumps(tmp_j)

        return str_anonymize(p_any)
    elif type(p_any)==int:
        return int_anonymize(p_any)
    elif type(p_any)==float:
        return float_anonymize(p_any)
    elif p_any is None:
        return p_any
    elif type(p_any)==list:
        for idx,le in enumerate(p_any):
            p_any[idx] = any_anonymize(le)
        return p_any
    elif type(p_any)==dict:
        dict_anonymize(p_any)
        return p_any 
    else:
        #print("------>"+str(type(p_any))+";"+str(p_any))
        return str_anonymize(str(p_any));
    #TODO : date data coverage


def anonymize_json_file(p_file_name:str) -> dict:
    with open(p_file_name) as jsonFile:
        j = json.load(jsonFile)
        dict_anonymize(j)
        return j
        

if __name__ == '__main__':
    aj = anonymize_json_file(sys.argv[1])
    print( json.dumps(aj) )
