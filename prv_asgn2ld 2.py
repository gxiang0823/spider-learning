# -*- coding: utf-8 -*-
#"""Module Providing Function Finding PR assignee's Leader."""
#######################################################################
# FileName:    prv_asgn2ld.py                                         #
# Author:      baotia6n                                               #
# Create:      2023-12-19                                             #
# UpDate:      2024-02-29                                             #
# Version:     v0.4                                                   #
# Notes:                                                              #
#      1. Manually copy the JSESSIONID into the console.              #
#      2. Current JSESSIONID can be found in Nexus website's Cookies. #
#      3. This Program CAN NOT deal with PRs that assignee is empty.  #
#######################################################################

# workflow note:
# 1. GET: /cp-validation?search=release==%222312.5000%22;changePackage.pbu==%22cam%22;flag=in=(C,F)
#   + JSESSIONID
#   ----> get callId set
# 2. POST: /calls/search?p=0&n=-1&s=id&d=asc
#   + callId list
#   ----> content list

import json
import sys
import requests


class Leader:
    """Class to organize data related to a leader."""
    #pr = []
    #er = []
    #assignee_set = set()

    def __init__(self, leader_id: str):
        self.id = leader_id
        self.pr = []
        self.er = []
        self.assignee_set = set()

    def add_pr(self, pr_id: str, asgn_id: str):
        """Define a function to add PR-assignee tuple"""
        self.pr.append((pr_id, asgn_id))

    def add_er(self, er_id: str, asgn_id: str):
        """Define a function to add ER-assignee tuple"""
        self.er.append((er_id, asgn_id))

    def add_asgn(self, asgn_id: str):
        """Define a function to add assignee into set"""
        self.assignee_set.add(asgn_id)


def print_status_code_error(request_type: str, status_code):
    '''Print Request Failure'''
    print("*************************************************************")
    print("* " + request_type + " Request Failure, status code: "
        + str(status_code)
        + ", Please try again.")
    print("*************************************************************")

def handle_get_response(get_response):
    ''' GET Request Failure and Check PR List'''
    if get_response.status_code != 200:
        print_status_code_error("GET", get_response.status_code)
        sys.exit(0)
    elif get_response.text == '[]':
        print("*************************************************************")
        print("* Request PR List is Empty, Please try again.               *")
        print("*************************************************************")
        sys.exit(0)

def build_call_id_set(get_resp_txt: str, call_id_set: set):
    '''get callId set'''
    get_raw_data = json.loads(get_resp_txt)
    for _item in get_raw_data:
        if _item["callId"] is not None:
            call_id_set.add(str(_item["callId"]))
    return call_id_set

def build_team_data(post_resp_txt: str, teams: dict):
    '''Build Leader ID to Leader Object Dict'''
    post_raw_data = json.loads(post_resp_txt)
    content_list = post_raw_data['content']

    for ct in content_list:
        call_type = ct['currentCallType']

        if call_type['value'] == 'ER':
            # Get ER's assigneeId and leaderId
            er = ct['er']
            assignee = er['assignee']
            er_id = str(er['id'])
            asgn_id = str(assignee['id'])
            leader_id = str(assignee['leaderId'])

            # Create new Leader Object
            if leader_id not in teams:
                teams[leader_id] = Leader(leader_id)

            # Store PR and assigneeId
            team = teams[leader_id]
            team.add_asgn(asgn_id)
            team.add_er(er_id, asgn_id)

        elif call_type['value'] == 'PR':
            # Get PR's assigneeId and leaderId
            pr = ct['pr']
            pr_assignee = pr['assignee']
            pr_id = str(pr['id'])
            asgn_id = str(pr_assignee['id'])
            leader_id = str(pr_assignee['leaderId'])

            # Create new Leader Object
            if leader_id not in teams:
                teams[leader_id] = Leader(leader_id)

            # Store PR and assigneeId
            team = teams[leader_id]
            team.add_asgn(asgn_id)
            team.add_pr(pr_id, asgn_id)

def output_result(file_name: str, teams: dict):
    '''Write Result into TXT'''
    with open(file_name, 'w', encoding='utf8') as file:
        for ld_id, ld in teams.items():
            file.write("leadid: " + ld_id + "\n")
            asgn_list = ""
            num = len(ld.assignee_set)
            # Output callId and assigneeId list
            file.write("PR account: " + str(len(ld.pr)) + "\n")
            for v in ld.pr:
                s = "    "+v[0]+" "+v[1]
                file.write(s+"\n")
            file.write("ER account: " + str(len(ld.er)) + "\n")
            if len(ld.er) != 0:
                for v in ld.er:
                    s = "    "+v[0]+" "+v[1]
                    file.write(s+"\n")
            file.write("total assignee: " + str(num) + "\n")
            # Output different Group's Info
            if "hwangb" in ld.assignee_set:
                file.write("    assigneeid: hwangb\t-> "
                        "managed mode CAM PRs for Ravneet (hwangb)\n")
                ld.assignee_set.remove("hwangb")
            for asgn in ld.assignee_set:
                asgn_list += (asgn + ", ")
            asgn_list = asgn_list[:-2]
            if ld_id == "buerer":
                # Check ASGN_LIST
                if len(asgn_list) != 0:
                    file.write("    assigneeid: [else]\t-> "
                            "CMM PR for Jeff Moffatt ("
                            + asgn_list + ")\n")
            elif ld_id == "vanterve":
                file.write("    assigneeid: [all]\t-> "
                        "Fixed Plane Additive PRs for Sagar ("
                        + asgn_list + ")\n")
            elif ld_id == "paradise":
                file.write("    assigneeid: [all]\t-> "
                        "CAM Machining PRs for Eric and the interns ("
                        + asgn_list + ")\n")
            else:
                file.write("    assigneeid: [OTHER]\t-> (" + asgn_list + ")\n")
            file.write("\n")

# Input Release and Cookies
print("****************************************************************")
release = input("* Enter Release: ")
print("* Pass/Fail/Needs Validation/Unable to Verify/Partial Fix/None *")
validation = input("* Enter Validation status: ")
print("* Current JSESSIONID can be found in Nexus website's Cookies.  *")
print("* Please Manually copy the JSESSIONID into the console.        *")
cookies_input = input("* Enter current JSESSIONID: ")
print("****************************************************************")
cookies = {'JSESSIONID': cookies_input}

# TEST COOKIES
# cookies = {'JSESSIONID':'019CA238E60C160834984753829B143A'}

# GET Request
GET_URL = 'https://nxrelmgtapi.net.plm.eds.com:7373/cp-validation'
getParam = {'search': 'release=="' + release
            + '";changePackage.pbu=="cam";'}
if validation != "None" and len(validation) != 0:
    getParam["search"] +='validation.status=="' + validation + '";'
getParam["search"] += 'flag=in=(C,F)'
getResponse = requests.get(
    GET_URL,
    cookies=cookies,
    params=getParam,
    verify=False,
    timeout=2000
)

handle_get_response(getResponse)
callIdSet = set()
build_call_id_set(getResponse.text, callIdSet)

print(callIdSet)

# POST Request
POST_URL = "https://nxrelmgtapi.net.plm.eds.com:7373/calls/search"
postHeader = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8"
}
postParam = {'p': '0', 'n': '-1', 's': 'id', 'd': 'asc'}

# build POST Request Payload
POST_QUERY = "id=in=("
for callId in callIdSet:
    POST_QUERY += (callId+',')
POST_QUERY = POST_QUERY[:-1]+')'
postPayload = '''{"query":"''' + POST_QUERY \
    + '''","aggregations":[],"filters":[],"fields":[]}'''

postResponse = requests.post(
    POST_URL,
    headers=postHeader,
    cookies=cookies,
    params=postParam,
    verify=False,
    data=postPayload,
    timeout=6000
)

# POST Request Failure
if postResponse.status_code != 200:
    print_status_code_error("POST", postResponse.status_code)
    sys.exit(0)

# Build Team Data
result = {}
build_team_data(postResponse.text, result)

# Create File Name
FILE_NAME = "result_" + release + "_"
if validation != "None" and len(validation) != 0:
    FILE_NAME += validation
FILE_NAME += ".txt"

# Write Results into TXT
output_result(FILE_NAME, result)

print("*******************************************************"
      "****************")
print("* The results are recorded in " + FILE_NAME +
      " in the current folder *")
print("*******************************************************"
      "****************")
