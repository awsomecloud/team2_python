from __future__ import print_function
from boto3.session import Session
import boto3
from texttable import Texttable
from urllib.request import Request, urlopen, URLError, HTTPError
import datetime
import json
import logging
import base64

session_main = boto3.session.Session()
HOOK_URL = "https://hooks.slack.com/services/"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

css = """
<html>
<head>
<style type=\"text/css\">
table {
color: #333;
font-family: Helvetica, Arial, sans-serif;
width: 1200px;
border-collapse:
collapse; 
border-spacing: 0;
}

td, th {
border: 1px solid transparent; /* No more visible border */
height: 30px;
}

th {
background: #DFDFDF; /* Darken header a bit */
text-align: center;
font-weight: bold;
}

td {
background: #FAFAFA;
text-align: center;
}

table tr:nth-child(odd) td{
background-color: white;
}
</style>
</head>
"""

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
first_html = "<body>" + nowDatetime + """
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>No.</th>
      <th>ID</th>
      <th>Name</th>
      <th>Type</th>
      <th>Protocol</th>
      <th>Port Range</th>
      <th>Source</th>
      <th>Description</th>
    </tr>
  </thead>
<tbody>
"""
last_html = """  
  </tbody>
</table>
</body>
</html>
"""


def lambda_handler(event, context):
    token_enkey = event['token']

    token = kms_d_function(token_enkey)

    channels_list = event['channels']
    for channel_info in channels_list:
        main(channel_info, token)

def kms_d_function(enkey):

    kms = session_main.client('kms')
    binary_data = base64.b64decode(enkey)
    meta = kms.decrypt(CiphertextBlob=binary_data)
    plaintext = meta[u'Plaintext']
    dekey = plaintext.decode()
    return dekey

def send_slack(token, channel_id, filename, title, comment):
    now = datetime.datetime.now()

    s3 = session_main.client("s3")
    file_name = "/tmp/sg_info.html"
    bucket = "mz-ea2-project-slack-log"
    now_time = str(now.strftime('%Y-%m-%d-%H:%M:%S'))
    object_name = title + "/" + now_time + "/" + title + now_time + '.html'
    s3_response = s3.upload_file(file_name, bucket, object_name,
                                 ExtraArgs={'ContentType': 'text/html', 'ACL': 'public-read'})

    link = 'https://mz-ea2-project-slack-log.s3.ap-northeast-2.amazonaws.com/' + title + "/" + now_time + "/" + title + now_time + '.html'
    print(s3_response)

    slack_message = {
        "username": "BIMO",
        "channel": "#describe-sg-vul-policy",
        "icon_url": "https://ca.slack-edge.com/T0ADM364S-UHC8WDMLP-5c50791074b2-48",
        "type": "modal",
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*취약 보안그룹 정보*",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*프로젝트 명 :* \n" + title + "\n*체크 시간 :* \n" + str(now_time) + "\n*취약 보안그룹 Url :* \n" + link,
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/approvalsNewDevice.png",
                    "alt_text": "computer thumbnail"
                }
            },
            {
                "type": "divider"
            }
        ]
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode(encoding='UTF8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)


def main(channel_info, token):
    ak_id = kms_d_function(channel_info['ak_id'])
    sk_id = kms_d_function(channel_info['sk_id'])

    session = Session(aws_access_key_id=ak_id,
                      aws_secret_access_key=sk_id)
    client = session.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    comment = channel_info['comment']
    title = channel_info['title']
    file_name = channel_info['file_name']
    channel_id = channel_info['channel_id']
    region_cd = channel_info['region_cd']
    region_list = region_cd.split(',')
    if region_list[0] == 'all':
        region_cd = regions
    else:
        region_cd = region_list
    type_cd = channel_info['type_cd']

    type_ao = 0  # 0 : all , 1 : open
    text_result = ''

    if type_cd == 'all':
        type_ao = 1
        x = get_sg_table_1(type_ao, region_cd, session)
        text_to_html(x)

        # text_result = x.draw()
    elif type_cd == 'open':
        type_ao = 2
        x = get_sg_table_1(type_ao, region_cd, session)
        text_to_html(x)
        # text_result = x.draw()
    else:
        print("error")

    # send_slack(token, channel_id, filename, title, comment)
    send_slack(token, channel_id, file_name, title, comment)



def get_sg_table_1(ao, region_cd, session):
    p_data = []
    table = Texttable(200)

    table.set_cols_align(["c", "l", "l", "l", "c", "c", "r"])
    table.set_cols_valign(["m", "m", "m", "t", "t", "t", "t"])

    # See if any argument was passed. First argument is the script name, skip that one (-1)
    #arguments = len(argv) - 1

    # Explicitly declaring variables here grants them global scope
    sgs = ""
    cidr_block = ""
    ip_protpcol = ""
    from_port = ""
    to_port = ""
    port_range = ""
    from_source = ""
    p_data.append(["region", "Group-Name", "Group-ID", "type", "Protocol", "Port", "Source/Destination"])
    # print("%s,%s,%s,%s,%s,%s" % ("Group-Name","Group-ID","In/Out","Protocol","Port","Source/Destination"))
    region_arr = region_cd
    for region in region_arr:
        ec2 = session.client('ec2', region)
        sgs = ec2.describe_security_groups()["SecurityGroups"]

        for sg in sgs:
            group_name = sg['GroupName']
            group_id = sg['GroupId']
            # InBound permissions ##########################################
            inbuond = sg['IpPermissions']
            p_Inbound = ""
            p_ip_protpcol = ""
            p_port_range = ""
            p_cidr_block = ""
            for rule in inbuond:
                port_range = "All"
                if rule['IpProtocol'] == "-1":
                    traffic_type = "All Traffic"
                    ip_protpcol = "All"
                    to_port = "All"
                else:
                    ip_protpcol = rule['IpProtocol']
                    from_port = rule['FromPort']
                    to_port = rule['ToPort']
                    if from_port == to_port:
                        port_range = from_port
                    else:
                        port_range = str(from_port) + ' - ' + str(to_port)
                    # If ICMP, report "N/A" for port #
                    if to_port == -1:
                        to_port = "N/A"

                # Is source/target an IP v4?
                if len(rule['IpRanges']) > 0:
                    for ip_range in rule['IpRanges']:
                        cidr_block = ip_range['CidrIp']
                        if ao == 2:
                            if ip_protpcol == 'All' or port_range == '' or port_range == '0 - 65535' or cidr_block == '0.0.0.0/0' or port_range == 'All':
                                p_Inbound += "Inbound" + "\n"
                                p_ip_protpcol += ip_protpcol + "\n"
                                p_port_range += str(port_range) + "\n"
                                p_cidr_block += cidr_block + "\n"
                        else:
                            p_Inbound += "Inbound" + "\n"
                            p_ip_protpcol += ip_protpcol + "\n"
                            p_port_range += str(port_range) + "\n"
                            p_cidr_block += cidr_block + "\n"

                # Is source/target an IP v6?
                if len(rule['Ipv6Ranges']) > 0:
                    for ip_range in rule['Ipv6Ranges']:
                        cidr_block = ip_range['CidrIpv6']
                        if ao == 2:
                            if ip_protpcol == 'All' or port_range == '' or port_range == '0 - 65535' or cidr_block == '0.0.0.0/0' or port_range == 'All':
                                p_Inbound += "Inbound" + "\n"
                                p_ip_protpcol += ip_protpcol + "\n"
                                p_port_range += str(port_range) + "\n"
                                p_cidr_block += cidr_block + "\n"
                        else:
                            p_Inbound += "Inbound" + "\n"
                            p_ip_protpcol += ip_protpcol + "\n"
                            p_port_range += str(port_range) + "\n"
                            p_cidr_block += cidr_block + "\n"

                # Is source/target a security group?
                if len(rule['UserIdGroupPairs']) > 0:
                    for source in rule['UserIdGroupPairs']:
                        if ao == 2:
                            if ip_protpcol == 'All' or port_range == '' or port_range == '0 - 65535' or port_range == 'All':
                                from_source = source['GroupId']
                                sg_info = ec2.describe_security_groups(GroupIds=[from_source])["SecurityGroups"]
                                from_name = sg_info[0]['GroupName']
                                p_Inbound += "Inbound" + "\n"
                                p_ip_protpcol += ip_protpcol + "\n"
                                p_port_range += str(port_range) + "\n"
                                p_cidr_block += from_source + '(' + from_name + ')' + "\n"
                        else:
                            from_source = source['GroupId']
                            sg_info = ec2.describe_security_groups(GroupIds=[from_source])["SecurityGroups"]
                            from_name = sg_info['GroupName']
                            p_Inbound += "Inbound" + "\n"
                            p_ip_protpcol += ip_protpcol + "\n"
                            p_port_range += str(port_range) + "\n"
                            p_cidr_block += from_source + '(' + from_name + ')' + "\n"
            if p_Inbound != "" or p_ip_protpcol != "" or p_port_range != "" or p_cidr_block != "":
                #table.add_rows = ([region, group_name, group_id, p_Inbound, p_ip_protpcol, p_port_range, p_cidr_block])
                p_data.append((region, group_name, group_id, p_Inbound[:-1], p_ip_protpcol[:-1], p_port_range[:-1], p_cidr_block[:-1]))
    print(p_data)
    #table.add_rows(p_data)
    return p_data


def text_to_html(result):

    text_file = open("/tmp/sg_info.html", "w")

    # write CSS
    text_file.write(css)
    text_file.write(first_html)

    html_table_index = ''
    num = 0
    print("-----------------")
    print(result)
    for sg_info in result:
        if num > 0:
            sg_num = len(sg_info[3].split('\n'))
            print(sg_num)
            region = sg_info[0]
            group_name = sg_info[1]
            group_id = sg_info[2]
            type_list = sg_info[3].split('\n')
            protocol_list = sg_info[4].split('\n')
            port_list = sg_info[5].split('\n')
            source_list = sg_info[6].split('\n')

            for i in range(sg_num):
                html_table_index = ''
                if i == 0:
                    html_table_index += "<tr>"
                    html_table_index += "<th rowspan=\""+ str(sg_num) +"\">" + str(num) + "</th>"
                    html_table_index += "<td rowspan=\""+ str(sg_num) +"\">" + region + "</td>"
                    html_table_index += "<td rowspan=\""+ str(sg_num) +"\">" + group_name + "</td>"
                    html_table_index += "<td rowspan=\""+ str(sg_num) +"\">" + group_id + "</td>"
                    html_table_index += "<td>" + type_list[i] + "</td>"
                    html_table_index += "<td>" + protocol_list[i] + "</td>"
                    html_table_index += "<td>" + port_list[i] + "</td>"
                    html_table_index += "<td>" + source_list[i] + "</td>"
                    html_table_index += "</tr>"
                    text_file.write(html_table_index)
                else:
                    html_table_index += "<tr>"
                    html_table_index += "<td>" + type_list[i] + "</td>"
                    html_table_index += "<td>" + protocol_list[i] + "</td>"
                    html_table_index += "<td>" + port_list[i] + "</td>"
                    html_table_index += "<td>" + source_list[i] + "</td>"
                    html_table_index += "</tr>"
                    text_file.write(html_table_index)
        num += 1
    text_file.write(last_html)
    text_file.close()
    return ''

if __name__ == '__main__':
    print('Console to slack sg started')