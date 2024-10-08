import os.path
import sys
import urllib.parse
import urllib.request
from operator import index

import numpy as np
import pandas as pd
import requests
import json

from sympy import false

requests.packages.urllib3.disable_warnings()


def down_load(data_json):
    formatted_data = json.dumps(data_json, indent=4, ensure_ascii=False)
    with open('cp_validation.json', 'w', encoding='utf-8') as fp:
        fp.write(formatted_data)


def Get_Request(release, pbu, validation, cookie):
    get_url = 'https://nexus.net.plm.eds.com:7373/cp-validation?'
    get_data = {
        'search': 'release=="' + release + '";changePackage.pbu=="' + pbu + '";validation.status=="' + validation + '";flag=in=(C,F)'}
    get_data = urllib.parse.urlencode(get_data)
    G_url = get_url + get_data
    get_headers = {'Cookie': cookie}

    get_request = urllib.request.Request(url=G_url, headers=get_headers)
    get_response = urllib.request.urlopen(get_request)
    get_content = get_response.read().decode('utf-8')
    get_data_json = json.loads(get_content)

    Call_ID_Set = set()
    for item in get_data_json:
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
    post_data_json = json.loads(post_content)

    # Down Load PR information

    # down_load(post_data_json)

    return post_data_json


def Get_Leader_Info(leader, item):
    Assignee_Info = item['Assignee_ID'].unique()
    if leader == 'buerer':
        output_info = ", ".join(Assignee_Info)
        print(f"Assignee ID: [else]\t-> CMM PR for Jeff Moffatt [{output_info}]\n")
    elif leader == 'vanterve':
        output_info = ", ".join(Assignee_Info)
        print(f"Assignee ID: [all]\t-> Fixed Plane Additive PRs for Sagar [{output_info}]\n")
    elif leader == 'paradise':
        output_info = ", ".join(Assignee_Info)
        print(f"Assignee ID: [all]\t-> CAM Machining PRs for Eric and the interns [{output_info}]\n")
    else:
        output_info = ", ".join(Assignee_Info)
        print(f"Assignee ID: [other]-> [{output_info}]\n")


def Check_data(Call_ID_Set):
    if not Call_ID_Set:
        print("*************************************************************")
        print("*        Request PR List is Empty, Please try again.        *")
        print("*************************************************************")
        sys.exit(0)


def Data_Process(post_data_json, release, validation):
    Rows = []
    Save_Info = []
    content_list = post_data_json['content']
    for ct in content_list:
        call_type = ct['currentCallType']
        application = ct['application']
        if call_type['value'] == 'ER':
            Call_Type = 'ER'
            er = ct['er']
            assignee = er['assignee']
            Call_ID = str(er['id'])
            Assignee_ID = str(assignee['id'])
            Assignee_Email = str(assignee['email'])
            Leader_ID = str(assignee['leaderId'])
            Supervisor_ID = str(assignee['supervisorId'])
            firstName = str(assignee['firstName'])
            lastName = str(assignee['lastName'])
            Name = firstName + " " + lastName
            Rows.append({'Call_ID': Call_ID, 'Call_Type': Call_Type, 'Assignee_ID': Assignee_ID,
                         'Assignee_Email': Assignee_Email, 'Leader_ID': Leader_ID, 'Supervisor_ID': Supervisor_ID,
                         'application': application})
            Save_Info.append({'Dev_ID': Assignee_ID,
                              'Dev_Email': Assignee_Email, 'Dev_Name': Name, 'Leader_ID': Leader_ID,
                              'Supervisor_ID': Supervisor_ID})
        elif call_type['value'] == 'PR':
            Call_Type = 'PR'
            pr = ct['pr']
            assignee = pr['assignee']
            Call_ID = str(pr['id'])
            Assignee_ID = str(assignee['id'])
            Assignee_Email = str(assignee['email'])
            Leader_ID = str(assignee['leaderId'])
            Supervisor_ID = str(assignee['supervisorId'])
            firstName = str(assignee['firstName'])
            lastName = str(assignee['lastName'])
            Name = firstName + " " + lastName
            Rows.append({'Call_ID': Call_ID, 'Call_Type': Call_Type, 'Assignee_ID': Assignee_ID,
                         'Assignee_Email': Assignee_Email, 'Leader_ID': Leader_ID, 'Supervisor_ID': Supervisor_ID,
                         'application': application})
            Save_Info.append({'Dev_ID': Assignee_ID,
                              'Dev_Email': Assignee_Email, 'Dev_Name': Name, 'Leader_ID': Leader_ID,
                              'Supervisor_ID': Supervisor_ID})

    # Save/Update developer information
    Dev_Info = pd.DataFrame(Save_Info)
    Now_Dev_Info = Dev_Info.drop_duplicates()
    Info_file_path = 'Assignee_Info.csv'
    if os.path.exists(Info_file_path):
        Dev_Info_csv = pd.read_csv(Info_file_path)
        new_items = Now_Dev_Info.merge(Dev_Info_csv, how='left', indicator=True).query('_merge == "left_only"').drop(
            '_merge', axis=1)
        Update_Info = pd.concat([Dev_Info_csv, new_items], ignore_index=True)
        Update_Info.to_csv(Info_file_path, index=False)
    else:
        Now_Dev_Info.to_csv(Info_file_path, index=False)

    # Create File Name
    FILE_NAME = "result_" + release + "_"
    if validation != "None" and len(validation) != 0:
        FILE_NAME += validation
    FILE_NAME += ".txt"

    # Save of assignee information
    Final_Result = pd.DataFrame(Rows)
    pr_groups = {leader_id: group for leader_id, group in Final_Result.groupby('Leader_ID')}

    original_stdout = sys.stdout
    with open(FILE_NAME, 'w') as file:
        sys.stdout = file
        for leader, item in pr_groups.items():
            print(f"Leader_ID:   {leader}")
            if leader == "vanterve":
                item.loc[item['application'] == 'CAM', 'Call_ID'] = '*' + item['Call_ID']
            print(item[['Call_ID', 'Call_Type', 'Assignee_ID', 'Supervisor_ID']].to_string(index=False))
            PR_Num = item[item['Call_Type'] == 'PR'].shape[0]
            ER_Num = item[item['Call_Type'] == 'ER'].shape[0]
            Assignee_Info = item['Assignee_ID'].unique()
            print(f"PR Num: {PR_Num}    ER Num: {ER_Num}    total assignee: {len(Assignee_Info)}")
            print("\n")

        # Classification of assignee information
        assignee_buerer = Final_Result[(Final_Result['Leader_ID'] == 'buerer')]['Assignee_ID'].unique()
        output_buerer = ", ".join(assignee_buerer)
        print(f"Assignee ID: [else]\t-> CMM PR for Jeff Moffatt [{output_buerer}]\n")

        assignee_vanterve = Final_Result[(Final_Result['Leader_ID'] == 'vanterve') & (Final_Result['application'] == 'ADD_FIXED_PLANE')]['Assignee_ID'].unique()
        output_vanterve = ", ".join(assignee_vanterve)
        print(f"Assignee ID: [all]\t-> Fixed Plane Additive PRs for Sagar [{output_vanterve}]\n")

        assignee_vanterve_remain = Final_Result[(Final_Result['Leader_ID'] == 'vanterve') & (Final_Result['application'] != 'ADD_FIXED_PLANE')]['Assignee_ID'].unique()
        assignee_paradise_in = Final_Result[(Final_Result['Leader_ID'] == 'paradise')]['Assignee_ID'].unique()
        assignee_paradise = pd.Series(pd.concat([pd.Series(assignee_paradise_in), pd.Series(assignee_vanterve_remain)]).unique())
        output_paradise = ", ".join(assignee_paradise)
        print(f"Assignee ID: [all]\t-> CAM Machining PRs for Eric and the interns [{output_paradise}]\n")

        assignee_else = Final_Result[(Final_Result['Leader_ID'] != 'buerer') & (Final_Result['Leader_ID'] != 'vanterve') & (Final_Result['Leader_ID'] != 'paradise')]['Assignee_ID'].unique()
        output_else = ", ".join(assignee_else)
        print(f"Assignee ID: [other]-> [{output_else}]\n")



    sys.stdout = original_stdout


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
    release = "2406.4000"
    pbu = "cam"
    validation = "Pass"
    cookie = "JSESSIONID=7A3C039FD5F28CAF83101C5DEA875CD6"
    # Get Call ID set
    Call_ID_Set = Get_Request(release, pbu, validation, cookie)
    # Check Call ID set
    Check_data(Call_ID_Set)
    # Get assignee information
    post_data_json = Post_Request(Call_ID_Set, cookie)
    # Process the information & output
    Data_Process(post_data_json, release, validation)
