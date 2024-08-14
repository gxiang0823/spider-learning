import urllib.parse
import urllib.request
import requests
import json

def down_load(data_json):
    formatted_data = json.dumps(data_json, indent=4, ensure_ascii=False)
    with open('cp_validation.json', 'w', encoding='utf-8') as fp:
        fp.write(formatted_data)

def Get_Request(release, pbu, validation, cookie):
    get_url = 'https://nexus.net.plm.eds.com:7373/cp-validation?'
    get_data = {'search': 'release=="' + release + '";changePackage.pbu=="' + pbu + '";validation.status=="' + validation + '";flag=in=(C,F)'}
    get_data = urllib.parse.urlencode(get_data)
    G_url = get_url + get_data
    get_headers = {'Cookie': cookie}

    get_request = urllib.request.Request(url=G_url, headers=get_headers)
    get_response = urllib.request.urlopen(get_request)
    get_content = get_response.read().decode('utf-8')
    data_json = json.loads(get_content)
    # down_load(data_json)

    Call_ID_Set = set()
    for item in data_json:
        if item["callId"] is not None:
            Call_ID_Set.add(str(item["callId"]))

    return Call_ID_Set

def Post_Request(Call_ID_Set, cookie):
    post_url = 'https://nxrelmgtapi.net.plm.eds.com:7373/calls/search?'
    post_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cookie
    }
    post_param = {'p': '0', 'n': '-1', 's': 'id', 'd': 'asc'}

    # build POST Request Payload
    post_query = "id=in=("
    for callId in Call_ID_Set:
        post_query += (callId + ',')
    post_query = post_query[:-1] + ')'
    post_payload = '''{"query":"''' + post_query \
                  + '''","aggregations":[],"filters":[],"fields":[]}'''

    post_response = requests.post(
        post_url,
        headers=post_headers,
        params=post_param,
        verify=False,
        data=post_payload,
        timeout=6000
    )
    post_content = post_response.content
    data_json = json.loads(post_content)
    print(data_json)



if __name__ == '__main__':
    # Input Release and Cookies
    # print("****************************************************************")
    # release = input("* Enter Release: ")
    # pbu = input("* PBU: ")
    # print("* Pass/Fail/Needs Validation/Unable to Verify/Partial Fix/None *")
    # validation = input("* Enter Validation status: ")
    # print("* Current JSESSIONID can be found in Nexus website's Cookies.  *")
    # print("* Please Manually copy the JSESSIONID into the console.        *")
    # cookie = input("* Enter your cookie: ")
    # print("****************************************************************")

    # test code
    release = "2406.3000"
    pbu = "cam"
    validation = "Pass"
    cookie = "JSESSIONID=894ACADFC6C8541EFC8F304F7A0DB013"

    Call_ID_Set = Get_Request(release, pbu, validation, cookie)

    Post_Request(Call_ID_Set, cookie)

