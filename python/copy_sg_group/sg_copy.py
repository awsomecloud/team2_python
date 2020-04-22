from boto3.session import Session
from ast import literal_eval

#-----복사에 필요 정보------
#리전 코드
region = "ap-northeast-2"
#복사하려는 vpc id
from_vpc_id = "vpc-"
#붙여넣으려는 vpc id
to_vpc_id = "vpc-"
#계정 정보
access_key = ''
secret_key = ''
#계정이 다른경우
# an_access_key = ''
# an_secret_key = ''
#태그 변경여부 및 값
tag_change = True
tag_from = 'poc-'
tag_to = 'prd-'
#------------여기까지-------

#session 생성
session = Session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
ec2 = session.client('ec2', region_name=region)
#다른 계정에 복사해야 할경우 session 생성
# an_session = Session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
# an_ec2 = an_session.client('ec2', region_name=region)

#자동 생성 아웃바운드 Role 제거 위한 변수
default_egress = [{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'Ipv6Ranges': [], 'PrefixListIds': [], 'UserIdGroupPairs': []}]

#to_Role SG ID 수정 작업
def update_role(sg_list):
    sg_update_list = []

    for sg in sg_list:
        sg_to_info = sg
        if sg_to_info["to_in_roles"] != []:
            #print(sg_to_info["from_in_roles"])
            for sg_info in sg_list:
                sg_to_info["to_in_roles"] = literal_eval(str(sg_to_info["to_in_roles"]).replace(sg_info["from_sg_id"], sg_info["to_sg_id"]))
            print('인룰 출력 테스트1')
            print(sg_to_info["to_in_roles"])
        if sg_to_info["to_out_roles"] != []:
            for sg_info in sg_list:
                sg_to_info["to_out_roles"] = literal_eval(str(sg_to_info["to_out_roles"]).replace(sg_info["from_sg_id"], sg_info["to_sg_id"]))
        print('인룰 출력 테스트2')
        print(sg_to_info["to_in_roles"])
        sg_update_list.append(sg_to_info)

    return sg_update_list


#vpc 내 sg 그룹 전부 가저오기
def describe_securities(name, value):
    response = ec2.describe_security_groups(
        Filters=[{
            'Name': name,
            'Values': [value]
        }]
    )

    return response['SecurityGroups']

#복사 할 SG 데이터 정리 JSON 생성
def descirbe_sg_ids(vpc_id, tag_change):
    response = describe_securities('vpc-id', vpc_id)
    #print(response)
    sg_group_info = []
    for secid in response:
        # 초기화
        sg_tag = []
        sg_des = ''
        sg_name = ''
        sg_id = ''
        change_sg_tag = []
        sg_in_role = []
        sg_out_role = []
        # Item 별로 보안그룹 변수에 넣기
        for key, val in secid.items():
            if key == 'GroupId':
                sg_id = val
            if key == 'Tags':
                sg_tag = val
            if key == 'Description':
                sg_des = val
            if key == 'GroupName':
                sg_name = val
            if key == 'IpPermissions':
                sg_in_role = val
            if key == 'IpPermissionsEgress':
                sg_out_role = val
        #보안그룹 데이터 정리 입력
        print(sg_id)
        if sg_name != 'default':
            if tag_change:
                #태그 변경 활성화
                if sg_tag != []:
                    print(str(sg_tag).replace(tag_from, tag_to))
                    change_sg_tag = literal_eval(str(sg_tag).replace(tag_from, tag_to))
                    print(change_sg_tag)
                sg_info = {
                    "from_sg_name": sg_name,
                    "from_sg_id": sg_id,
                    "from_description": sg_des,
                    "from_Tag": sg_tag,
                    "from_in_roles": sg_in_role,
                    "from_out_roles": sg_out_role,
                    "to_sg_name": sg_name.replace(tag_from, tag_to),
                    "to_sg_id": None,
                    "to_description": sg_des.replace(tag_from, tag_to),
                    "to_Tag": change_sg_tag,
                    "to_in_roles": sg_in_role,
                    "to_out_roles": sg_out_role
                }
            else:
                sg_info = {
                    "from_sg_name": sg_name,
                    "from_sg_id": sg_id,
                    "from_description": sg_des,
                    "from_Tag": sg_tag,
                    "from_in_roles": sg_in_role,
                    "from_out_roles": sg_out_role,
                    "to_sg_name": sg_name,
                    "to_sg_id": None,
                    "to_description": sg_des,
                    "to_Tag": sg_tag,
                    "to_in_roles": sg_in_role,
                    "to_out_roles": sg_out_role
                }
            sg_group_info.append(sg_info)
    print(sg_group_info)
    return sg_group_info

#sg_list = ["sg-0666bb163fd40b0d7", "sg-076ebacf62c758e59"]
#sg_info_list = descirbe_sg_ids(from_vpc_id)

#필요없어질듯
# def dump_sg(client, sg_list):
#     print(sgids)
#     sg_info = client.describe_security_groups(
#             Filters=[{'Name': 'group-id', 'Values': sgids}])['SecurityGroups']
#     return sg_info

def copy_sg(tgt_client, sg_list):
    sg_num = 0
    for sg in sg_list:
        resp = tgt_client.create_security_group(
            GroupName=sg['to_sg_name'], Description=sg['to_description'], VpcId=to_vpc_id, )
        new_grp_id = resp['GroupId']
        print("Create SG {} - \"{}\" - \"{}\" in VPCID: {}".format(new_grp_id, sg['to_sg_name'], sg['to_description'],
                                                                   to_vpc_id))
        # Tag 있는 경우 등록
        if sg['to_Tag'] != []:
            ec2.create_tags(Resources=[new_grp_id], Tags=sg['to_Tag'])
        #ID 입력은 더 좋은 방법이 있을것으로 생각됨
        sg_list[sg_num]['to_sg_id'] = new_grp_id
        sg_num += 1

    update_sg_list = update_role(sg_list)

    for sg in update_sg_list:
        print('룰 입력 총정보 확인')
        print(sg)
        if sg.get('to_in_roles') != []:
            print('인바운드 입력')
            print(sg.get('to_sg_id'))
            print(sg.get('to_in_roles'))
            tgt_client.authorize_security_group_ingress(
                GroupId=sg.get('to_sg_id'), IpPermissions=sg.get('to_in_roles'))

        if sg.get('to_out_roles') != []:
            print('아웃 바운드 입력')
            print(sg.get('to_sg_id'))
            print(sg.get('to_out_roles'))
            #기존 아웃바운드 룰 전부 삭제
            tgt_client.revoke_security_group_egress(
                GroupId=sg.get('to_sg_id'), IpPermissions=default_egress)
            tgt_client.authorize_security_group_egress(
                GroupId=sg.get('to_sg_id'), IpPermissions=sg.get('to_out_roles'))

    return ''

sg_info_list = descirbe_sg_ids(from_vpc_id, tag_change)
copy_sg(ec2, sg_info_list)