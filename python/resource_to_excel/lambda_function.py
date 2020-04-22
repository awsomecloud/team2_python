import pandas as pd
import boto3
from boto3.session import Session
import vpc_service, subnet_service, route_service, vpn_service, nat_service
import security_service, ec2_service, elb_service, rds_service, cloudfront_service
import alb_service, tg_service, vpc_peer_service
import s3_service, direct_connect_service, workspace_service, iam_service, efs_service
from slackclient import SlackClient
import sys
import base64

# Gathering vpc infos, name, id, cidr, flow logs
def get_vpc_info(tag_val, ec2, check_type):
    vpc = vpc_service.vpc(ec2)
    get_vpc = vpc.desecribe_vpc(tag_val, check_type)

    return get_vpc

# vpc_id is list type
def get_subnet_info(vpc_id, ec2):
    subnets = subnet_service.subnet(ec2)
    get_sub_info = subnets.describe_subnet(vpc_id)

    return get_sub_info


# subnet_id is list type
def get_route_info(ec2, vpc_id):
    routes = route_service.route(ec2)
    get_route_info = routes.describe_route(vpc_id)

    return get_route_info


# vpc_id is list type
def get_vpn_info(vpc_id, ec2):
    vpn = vpn_service.vpn(ec2)
    get_vpn_info = vpn.describe_vpn_gates(vpc_id)

    return get_vpn_info


# vpc_id is list type
def get_nat_info(vpc_id, ec2):
    nat = nat_service.nat(ec2)
    get_nat_info = nat.describe_nats(vpc_id)

    return get_nat_info


def get_securities_info(vpc_id, ec2, type):
    securities = security_service.security_groups(ec2, type)
    get_securities_info = securities.describe_ips(vpc_id)

    return get_securities_info


def get_instances_info(vpc_id, ec2):
    instances = ec2_service.ec2(ec2)
    get_ec2_info = instances.get_instance_ids(vpc_id)

    return get_ec2_info


def get_elbs_info(elb):
    elbs = elb_service.elb(elb)
    get_classic_elb_info = elbs.descrbie_classic_elb()

    result = get_classic_elb_info

    return result

#190516 alb 추가
def get_albs_info(vpc_id ,elbv2):
    albs =  alb_service.alb(vpc_id, elbv2) #elb_service 파일내의 alb class

    get_not_classic_elb_info = albs.describe_not_classic_elb()

    result = get_not_classic_elb_info

    return result

#190516 target group 추가
def get_tg_info(vpc_id, elbv2):
    tg = tg_service.tg(vpc_id, elbv2)
    get_target_group_info = tg.describe_target_groups()
    result = get_target_group_info

    return result


def get_rds_info(vpc_id, rds):
    rdss = rds_service.rds(vpc_id, rds)
    get_rds_info = rdss.get_db_arn()

    return get_rds_info


def get_cf_info(cf):
    cfs = cloudfront_service.cloudfront(cf)
    get_cfs_info = cfs.describe_cfs()

    return get_cfs_info


def get_s3_info(s3):
    s3s = s3_service.s3s(s3)
    get_s3s_info = s3s.describe_s3s()

    return get_s3s_info


def get_dx_info(direct):
    direct = direct_connect_service.direct_connect(direct)
    get_direct_connection = direct.describe_dx()

    return get_direct_connection

#190523 workspace 추가
def get_workspace_info(workspace, ec2, vpc_id):
    workspaces = workspace_service.ws(workspace, ec2, vpc_id)
    get_workspace_info = workspaces.describe_workspace_info()

    return get_workspace_info

#190524 iam 추가
def get_iam_info(iam, access_yn):
    iam = iam_service.iam(iam, access_yn)
    get_iam_info = iam.describe_iam_info()

    return get_iam_info

#190603 efs 추가
def get_efs_info(efs, ec2, vpc_id, region_id):
    efs = efs_service.ef(efs, ec2, vpc_id, region_id)
    get_efs_info = efs.describe_efs_info()

    return get_efs_info

# 191022 vpc peering 추가
def get_vpc_peer_info(ec2):
    vpc = vpc_peer_service.vpc_peer(ec2)
    get_vpc_peer = vpc.desecribe_vpc_peer()
    return get_vpc_peer


# gram 요청사항
def error_slack(token, channel_id):
    slack_client = SlackClient(token)
    slack_client.api_call('chat.postMessage', channel=channel_id, text='사용 불가능한 채널 입니다. 관리자에게 문의 바랍니다.')
    sys.exit(1)

def lambda_handler(event, context):
    token = ''
    check_type_vpc = ''

    #민걸mzesc
    if event['command'] == '/excel':
        token_enkey = 'AQICAHjrLt4RE2xJfsnejjfkYDdq/kH7U7ZPBe/lxzMeOCDOggHCx0qFiyGWwGlU8uAKtVo8AAAArTCBqgYJKoZIhvcNAQcGoIGcMIGZAgEAMIGTBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDBEPaHlJi6SX1tUGrQIBEIBmv8TRU9vTKc40iuGRm4ogyKisH3JSHWYPLNK+6Ov/kuKjUFVckn0Fs25CyiAoSHHiLdMjEP+eKMz+C45BEFc+hQjI51+wQ3D9QlvbnH/wN2R3DOdqSqG83iS+2yiVYvWeUuOs20jE'
        kms = boto3.client('kms')
        binary_data = base64.b64decode(token_enkey)
        meta = kms.decrypt(CiphertextBlob=binary_data)
        plaintext = meta[u'Plaintext']
        token = plaintext.decode()
        check_type_vpc = 'tag'
        channel_id = event['channel_id']
    elif event['command'] == '/excel01':
        token = ''
        check_type_vpc = 'id'
    elif event['command'] == '/gram-excel':
        token = ''
        if event['channel_id'] != 'GT2C0Q2F3':
            error_slack(token, event['channel_id'])
    else:
        token = ''
        check_type_vpc = 'id'

    slack_client = SlackClient(token)
    channel_id = event['channel_id']


    #슬렉 주석
    slack_client.api_call('chat.postMessage', channel=channel_id, text='aws resource -> excel 변환 시작')

    data_parameters = event['text'].split(' ')

    data_parameters_size = len(data_parameters)

    #print('받은 명령어 : ' + event['text'])
    print('받은 채널 : ' + event['channel_id'])
    print('사용 유저명 : ' + event['user_name'])

    # basic environment setting
    region = data_parameters[1]
    #profile_name = data_parameters[2]
    access_key = data_parameters[2]
    secret_key = data_parameters[3]

    #region = sys.argv[2]
    #profile_name = sys.argv[3]
    #access_key = sys.argv[4]
    #secret_key = sys.argv[5]

    # 리전 리스트, 리전명 배열
    region_code_list = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ca-central-1', 'eu-central-1',
                        'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'ap-east-1', 'ap-northeast-1',
                        'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ap-south-1', 'sa-east-1']
    region_name_list = ['N-Virginia', 'Ohio', 'N-California', 'Oregon', 'Central', 'Frankfurt',
                        'Ireland', 'London', 'Paris', 'Stockholm', 'Hong Kong', 'Tokyo',
                        'Seoul', 'Osaka-Local', 'Singapore', 'Sydney', 'Mumbai', 'São Paulo']

    region_name = ''
    if(data_parameters_size < 4):
        slack_client.api_call('chat.postMessage', channel='GJCF5MXL3', text='명령어를 잘못 입력 하셨습니다. helpme 를 통해 확인해주세요.')
    elif data_parameters_size == 5:
        xlsx_name = data_parameters[4]

    elif data_parameters_size == 4:
        for i, region_code_info in enumerate(region_code_list):
            if region_code_info == region:
                region_name = region_name_list[i]
        xlsx_name = 'aws_resources_' + data_parameters[0] + '_' + region_name + '.xlsx'


    #if profile_name != '':
    session = Session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    ec2 = session.client('ec2')
    elb = session.client('elb')
    elbv2 = session.client('elbv2')
    rds = session.client('rds')
    cf = session.client('cloudfront')
    s3 = session.client('s3')
    direct = session.client('directconnect')
    workspace = session.client('workspaces')
    iam = session.client('iam')
    efs = session.client('efs')

    #xlsx_name = sys.argv[3]

    writer_vpc_info = pd.ExcelWriter('/tmp/'+xlsx_name, engine='xlsxwriter')
    workbook = writer_vpc_info.book
    start_row = 3
    iam_start_row = 2
    #-----------------xlsx 디자인 용 -----------------------------
    # format to apply to xlsx
    border_format = workbook.add_format({
        'border': 1
    })
    # 중앙정렬 format
    center_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter'
    })
    # 헤더 배경 + 글씨 format
    header_format = workbook.add_format({
        'font_color': 'white',
        'border': 1,
        'bold': 1,
        'bg_color': 'black'
    })
    # A라인 bold 처리
    bold_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    # ----------------------------------------------------------
    tag_val = [data_parameters[0]]
    try:
        # get iam info
        iam_values = get_iam_info(iam, 'n')
        iam_labels = ['Account Number', '용도', 'AWS Management Console URL', 'ID', 'PW', 'Permission', '비고']
        df_iam = pd.DataFrame.from_records(iam_values, columns=iam_labels)
        df_iam.index += 1
        df_iam.to_excel(writer_vpc_info, sheet_name='3.AWS 접속정보', startrow=2)
        worksheet_iam = writer_vpc_info.sheets['3.AWS 접속정보']
        worksheet_iam.write(0, 0, '3.AWS 접속정보')
        worksheet_iam.write(iam_start_row, 0, '연번', center_format)

        st_row = 2
        ed_row = st_row + len(df_iam)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_iam.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_iam.set_column('B:H', 18, center_format)
        # 헤더 색,배경
        worksheet_iam.conditional_format(st_row, 0, st_row, len(iam_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # Iam 출력값
        worksheet_iam.conditional_format(st_row, 0, ed_row, len(iam_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        iam_start_row += len(df_iam)
        # print('iam info', df_iam)

        # get vpc info
        # tag_val = [sys.argv[1]]  # ['api_private_test']

        vpc_labels = ['Name', 'ID', 'CIDR', 'Flow Logs']
        vpc_values = get_vpc_info(tag_val, ec2, 'tag')
        df_vpc = pd.DataFrame.from_records(vpc_values, columns=vpc_labels)
        df_vpc.index += 1
        df_vpc.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=3)

        worksheet = writer_vpc_info.sheets['4.VPC 구성정보']
        worksheet.write(0, 0, '2. VPC 구성정보')
        worksheet.write(2, 0, '2.1 VPC 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = 3
        ed_row = st_row + len(df_vpc)

        # 포멧 설정
        # 중앙 정렬
        worksheet.set_column('B:Z', 18, center_format)
        # A라인 bold 처리
        worksheet.set_column('A:A', 18, bold_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(vpc_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(vpc_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_vpc) + 3
        # print('vpc info', len(df_vpc), df_vpc)

        # vpc_peer 테스트
        test = get_vpc_peer_info(ec2)

        # get subnet info
        vpc_ids = []
        for name, vpc_id, _, _ in vpc_values:
            vpc_ids.append(vpc_id)

        subnet_labels = ['Name', 'ID', 'VPC', 'CIDR', 'Route Table']
        sub_values = get_subnet_info(vpc_ids, ec2)
        df_subnet = pd.DataFrame.from_records(sub_values, columns=subnet_labels)
        df_subnet.index += 1
        df_subnet.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.2 Subnet 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_subnet)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(subnet_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(subnet_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_subnet) + 3
        # print('sub info', df_subnet)

        # get route info
        # sub_ids = []
        # for _, subid, _, _, _ in sub_values:
        #     sub_ids.append(subid)

        route_labels = ['Name', 'Route Table ID', 'Main']
        route_values = get_route_info(ec2, vpc_ids)
        df_route = pd.DataFrame.from_records(route_values, columns=route_labels)
        df_route.index += 1
        df_route.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.3 Route Table 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_route)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(route_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(route_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_route) + 3
        # print('route info', df_route)

        # get nat info
        nat_values = None
        nat_labels = ['ID', 'EIP', 'PIP', 'VPC', 'Subnet']
        for vid in vpc_ids:
            nat_values = get_nat_info(vid, ec2)
        print(nat_values)
        print(nat_values)
        df_nat = pd.DataFrame.from_records(nat_values, columns=nat_labels)
        df_nat.index += 1
        df_nat.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.5 NAT Gateway 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_nat)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(nat_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(nat_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_nat) + 3
        # print('nat info', df_nat)

        # get direct connect info
        direct_values = None
        direct_values = get_dx_info(direct)
        direct_labels = ['Name', 'ID', 'Connection', 'VGW', 'Your Peer IP', 'Amazon Peer IP']
        df_direct = pd.DataFrame.from_records(direct_values, columns=direct_labels)
        df_direct.index += 1
        df_direct.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.6 Direct Connect 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_direct)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(direct_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(direct_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_direct) + 3
        # print('DX info', df_direct)

        # get vpc_peer info
        vpc_peer_values = None
        vpc_peer_labels = ['Name', 'ID', 'Status', 'Requester VPC', 'Accepter VPC', 'Requester CIDR', 'Accepter CIDR',
                           'Requester VPC DNS', 'Accepter VPC DNS']

        vpc_peer_values = get_vpc_peer_info(ec2)

        df_vpc_peer_labels = pd.DataFrame.from_records(vpc_peer_values, columns=vpc_peer_labels)
        df_vpc_peer_labels.index += 1
        df_vpc_peer_labels.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.7 VPC Peering 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_vpc_peer_labels)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(vpc_peer_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(vpc_peer_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_vpc_peer_labels) + 3

        # 수정중
        # get vpn info
        vpn_values = None
        vpn_labels = ['Name', 'CGW ID', 'VPN ID', 'Customer IP', 'id_asn', 'tunnel1', 'tunnel2', 'static_routes', 'etc']

        for vid in vpc_ids:
            vpn_values = get_vpn_info(vid, ec2)
            # print('nat infoaaa :', vpn_values)
        df_vpn = pd.DataFrame.from_records(vpn_values, columns=vpn_labels)
        df_vpn.index += 1
        df_vpn.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.8 VPN 현황')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_vpn)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(vpn_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # vpc 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(vpn_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_vpn) + 3
        # print('vpn info', df_vpn)

        # get securties info
        security_values = None
        df_sg = pd.DataFrame()
        sg_labels = ['ID', 'Name', 'Type', 'Protocol', 'Port Range', 'Source', 'Description']
        for vid in vpc_ids:
            security_values = get_securities_info(vid, ec2, 'in')
        # print('security info', security_values)

        # --------------------------여기서 부터 ----------------------------------------------------
        sg_id_list = []
        sg_name_list = []
        sg_merge_list = []
        sg_id = ''
        sg_name = ''
        # print('보안그룹 시작 : ')
        # print(start_row)

        col_index = start_row + 2
        for col in security_values:
            start = col_index
            for sg_col in col:
                col_index += 1

            sg_id = sg_col[0]
            sg_name = sg_col[1]
            end = col_index - 1
            testtest = (start, end, sg_id, sg_name)
            sg_merge_list.append(testtest)

            # --------------------------여기 보면됨~~ ----------------------------------------------------
            df_to_append = pd.DataFrame.from_records(col, columns=sg_labels)
            df_sg = df_sg.append(df_to_append)
        df_sg.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.9 Security Group 현황(InBound)')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_sg)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(sg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(sg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_sg) + 3
        # print(df_sg)

        number_sg = 1
        for index in sg_merge_list:
            # print(index)
            if (index[1] - index[0]) == 0:
                worksheet.write(index[0] - 1, 0, str(number_sg), bold_format)
                worksheet.write(index[0] - 1, 1, index[2], center_format)
                worksheet.write(index[0] - 1, 2, index[3], center_format)
            else:
                worksheet.merge_range('A' + str(index[0]) + ':A' + str(index[1]), str(number_sg), bold_format)
                worksheet.merge_range('B' + str(index[0]) + ':B' + str(index[1]), index[2], center_format)
                worksheet.merge_range('C' + str(index[0]) + ':C' + str(index[1]), index[3], center_format)

            number_sg += 1

        # get securties info
        security_values = None
        df_sg = pd.DataFrame()
        sg_labels = ['ID', 'Name', 'Type', 'Protocol', 'Port Range', 'Destination', 'Description']
        for vid in vpc_ids:
            security_values = get_securities_info(vid, ec2, 'out')
        # print('security info', security_values)

        # --------------------------여기서 부터 ----------------------------------------------------
        sg_id_list = []
        sg_name_list = []
        sg_merge_list = []
        sg_id = ''
        sg_name = ''
        # print('보안그룹 시작 : ')
        # print(start_row)

        col_index = start_row + 2
        for col in security_values:
            start = col_index
            for sg_col in col:
                col_index += 1

            sg_id = sg_col[0]
            sg_name = sg_col[1]
            end = col_index - 1
            testtest = (start, end, sg_id, sg_name)
            sg_merge_list.append(testtest)

            # --------------------------여기 보면됨~~ ----------------------------------------------------
            df_to_append = pd.DataFrame.from_records(col, columns=sg_labels)
            df_sg = df_sg.append(df_to_append)
        df_sg.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
        worksheet.write(start_row - 1, 0, '2.10 Security Group 현황(OutBound)')
        worksheet.write(start_row, 0, '연번')

        st_row = start_row
        ed_row = st_row + len(df_sg)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet.conditional_format(st_row, 0, st_row, len(sg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet.conditional_format(st_row, 0, ed_row, len(sg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        start_row += len(df_sg) + 3
        # print(df_sg)

        number_sg = 1
        for index in sg_merge_list:
            # print(index)
            if (index[1] - index[0]) == 0:
                worksheet.write(index[0] - 1, 0, str(number_sg), bold_format)
                worksheet.write(index[0] - 1, 1, index[2], center_format)
                worksheet.write(index[0] - 1, 2, index[3], center_format)
            else:
                worksheet.merge_range('A' + str(index[0]) + ':A' + str(index[1]), str(number_sg), bold_format)
                worksheet.merge_range('B' + str(index[0]) + ':B' + str(index[1]), index[2], center_format)
                worksheet.merge_range('C' + str(index[0]) + ':C' + str(index[1]), index[3], center_format)

            number_sg += 1

        # get instance info
        instances_values = None
        ec2_start_row = 3
        df_ec2 = pd.DataFrame()
        ec2_labels = ['Name', 'Instance ID', 'Type', 'AZ', 'Key Pair', 'Security Group', 'IAM Role', 'EIP', 'PIP', 'ID',
                      'PW', 'EBS', 'OS', 'etc', 'UserData']

        # [민걸] 나중에 꼭 지워야함 vpn_value 출력
        for vid in vpc_ids:
            instances_values = get_instances_info(vid, ec2)

        ec2_to_append = pd.DataFrame.from_records(instances_values, columns=ec2_labels)
        df_ec2 = df_ec2.append(ec2_to_append)
        df_ec2.index += 1
        df_ec2.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=3)
        worksheet_ec2 = writer_vpc_info.sheets['5.EC2 현황정보']
        worksheet_ec2.write(0, 0, '3. EC2 현황정보')
        worksheet_ec2.write(2, 0, '3.1 Instance 현황')
        worksheet_ec2.write(ec2_start_row, 0, '연번')

        st_row = ec2_start_row
        ed_row = st_row + len(df_ec2)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_ec2.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_ec2.set_column('B:P', 18, center_format)
        # 헤더 색,배경
        worksheet_ec2.conditional_format(st_row, 0, st_row, len(ec2_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_ec2.conditional_format(st_row, 0, ed_row, len(ec2_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        ec2_start_row += len(df_ec2) + 3
        # print(df_ec2)

        # get elbs info
        elbs_values = get_elbs_info(elb)
        elb_labels = ['Name', 'DNS Name', 'Port', 'AZ', 'Host Count', 'Health Check']
        df_elbs = pd.DataFrame.from_records(elbs_values, columns=elb_labels)
        df_elbs.index += 1
        df_elbs.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
        worksheet_ec2.write(ec2_start_row - 1, 0, '3.2 CLB 현황')
        worksheet_ec2.write(ec2_start_row, 0, '연번')

        st_row = ec2_start_row
        ed_row = st_row + len(df_elbs)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet_ec2.conditional_format(st_row, 0, st_row, len(elb_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_ec2.conditional_format(st_row, 0, ed_row, len(elb_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        ec2_start_row += len(df_elbs) + 3
        # print('elb info ', df_elbs)

        # get albs info
        alb_labels = ['Name', 'DNS Name', 'ELB Type', 'AZ', 'Host Count']

        for vid in vpc_ids:
            albs_values = get_albs_info(vid, elbv2)
        df_albs = pd.DataFrame.from_records(albs_values, columns=alb_labels)
        df_albs.index += 1
        df_albs.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
        worksheet_ec2.write(ec2_start_row - 1, 0, '3.3 ELB 현황')
        worksheet_ec2.write(ec2_start_row, 0, '연번')

        st_row = ec2_start_row
        ed_row = st_row + len(df_albs)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet_ec2.conditional_format(st_row, 0, st_row, len(alb_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_ec2.conditional_format(st_row, 0, ed_row, len(alb_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        ec2_start_row += len(df_albs) + 3
        # print('elbv2 info ', df_albs)

        # get target group info
        for vid in vpc_ids:
            tg_values = get_tg_info(vid, elbv2)
        tg_labels = ['Name', 'Port', 'Health Protocol', 'Health Intervalseconds', 'Health timeoutseconds',
                     'Health ThresholdCount', 'UnHealth ThresholdCount', 'Health path', 'used alb']
        df_tg = pd.DataFrame.from_records(tg_values, columns=tg_labels)
        df_tg.index += 1
        df_tg.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
        worksheet_ec2.write(ec2_start_row - 1, 0, '3.4 Target Group 현황')
        worksheet_ec2.write(ec2_start_row, 0, '연번')

        st_row = ec2_start_row
        ed_row = st_row + len(df_tg)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet_ec2.conditional_format(st_row, 0, st_row, len(tg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_ec2.conditional_format(st_row, 0, ed_row, len(tg_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        # print('Target Group info ', df_tg)

        # get rds info
        for vid in vpc_ids:
            rds_values = get_rds_info(vid, rds)
        rds_labels = ['Name', 'DB Name', 'DB Engine', 'Type', 'Storage', 'ID', 'PW', 'Character Set', 'Multi-Az',
                      'Publicly', 'Endpoint', 'Security Groups', 'Subnet Group', 'Parameters / Option Groups']
        df_rds = pd.DataFrame.from_records(rds_values, columns=rds_labels)
        df_rds.index += 1
        df_rds.to_excel(writer_vpc_info, sheet_name='6.RDS 현황정보', startrow=2)
        worksheet_rds = writer_vpc_info.sheets['6.RDS 현황정보']
        worksheet_rds.write(0, 0, '4.RDS 현황정보')
        worksheet_rds.write(2, 0, '연번')

        st_row = 2
        ed_row = st_row + len(df_rds)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_rds.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_rds.set_column('B:O', 18, center_format)
        # 헤더 색,배경
        worksheet_rds.conditional_format(st_row, 0, st_row, len(rds_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_rds.conditional_format(st_row, 0, ed_row, len(rds_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        # print('rds info : ', df_rds)

        # get cf info
        cfs_values = get_cf_info(cf)
        cfs_labels = ['ID', 'Domain', 'Origin', 'CNAMEs', 'Etc']
        cf_start_row = 3
        df_cfs = pd.DataFrame.from_records(cfs_values, columns=cfs_labels)
        df_cfs.index += 1
        df_cfs.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
        worksheet_cf = writer_vpc_info.sheets['7.CloudFront&S3']
        worksheet_cf.write(0, 0, 'CloudFront&S3 현황정보')
        worksheet_cf.write(2, 0, '5.1CloudFront')
        worksheet_cf.write(3, 0, '연번')

        st_row = cf_start_row
        ed_row = st_row + len(df_cfs)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_cf.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_cf.set_column('B:F', 18, center_format)
        # 헤더 색,배경
        worksheet_cf.conditional_format(st_row, 0, st_row, len(cfs_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_cf.conditional_format(st_row, 0, ed_row, len(cfs_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        cf_start_row += len(df_cfs) + 3
        # print('cloud front info ', df_cfs)

        # get s3 info
        s3_values = get_s3_info(s3)
        s3_labels = ['Bucket Name', 'Region', 'Use', 'User', 'Authority']
        df_s3s = pd.DataFrame.from_records(s3_values, columns=s3_labels)
        df_s3s.index += 1
        df_s3s.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
        worksheet_cf.write(cf_start_row - 1, 0, '5.S3')
        worksheet_cf.write(cf_start_row, 0, '연번')

        st_row = cf_start_row
        ed_row = st_row + len(df_s3s)

        # 포멧 설정
        # 중앙 정렬
        # worksheet.set_column('A:Z', 18, center_format)
        # 헤더 색,배경
        worksheet_cf.conditional_format(st_row, 0, st_row, len(s3_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_cf.conditional_format(st_row, 0, ed_row, len(s3_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        # print(df_s3s)

        # get workspace info
        for vid in vpc_ids:
            workspace = get_workspace_info(workspace, ec2, vid)
        ws_labels = ['WorkSpace ID', 'Username', 'Compute', 'Running Mode', 'Root Volume', 'User Volume', 'Status']
        df_ws = pd.DataFrame.from_records(workspace, columns=ws_labels)
        df_ws.index += 1
        df_ws.to_excel(writer_vpc_info, sheet_name='8.Workspace 현황정보', startrow=2)
        worksheet_ws = writer_vpc_info.sheets['8.Workspace 현황정보']
        worksheet_ws.write(0, 0, '8.Workspace 현황정보')
        worksheet_ws.write(2, 0, '연번')

        st_row = 2
        ed_row = st_row + len(df_ws)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_ws.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_ws.set_column('B:H', 18, center_format)
        # 헤더 색,배경
        worksheet_ws.conditional_format(st_row, 0, st_row, len(ws_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_ws.conditional_format(st_row, 0, ed_row, len(ws_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        # print('workspace info : ', df_ws)

        # test efs
        for vid in vpc_ids:
            efs_info = get_efs_info(efs, ec2, vid, region)
        efs_labels = ['Name', 'ID', 'Size', 'Performance Mode', 'Mount Info', 'DNS', 'Security Groups']
        df_efs = pd.DataFrame.from_records(efs_info, columns=efs_labels)
        df_efs.index += 1
        df_efs.to_excel(writer_vpc_info, sheet_name='8.EFS 현황정보', startrow=2)
        worksheet_efs = writer_vpc_info.sheets['8.EFS 현황정보']
        worksheet_efs.write(0, 0, '8.EFS 현황정보')
        worksheet_efs.write(2, 0, '연번')

        st_row = 2
        ed_row = st_row + len(df_ws)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_efs.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_efs.set_column('B:H', 18, center_format)
        # 헤더 색,배경
        worksheet_efs.conditional_format(st_row, 0, st_row, len(efs_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_efs.conditional_format(st_row, 0, ed_row, len(efs_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        # print('workspace info : ', df_efs)

        # get accessKey info
        access_info = get_iam_info(iam, 'y')

        access_labels = ['ID', 'Access Key', 'Secret Access Key', 'Permission', '비고']
        df_access = pd.DataFrame.from_records(access_info, columns=access_labels)
        df_access.index += 1
        df_access.to_excel(writer_vpc_info, sheet_name='9.AccessKey', startrow=2)
        worksheet_access = writer_vpc_info.sheets['9.AccessKey']
        worksheet_access.write(0, 0, '9.AccessKey')
        worksheet_access.write(2, 0, '연번')

        st_row = 2
        ed_row = st_row + len(df_access)

        # 포멧 설정
        # A라인 bold 처리
        worksheet_access.set_column('A:A', 18, bold_format)
        # 중앙 정렬
        worksheet_access.set_column('B:H', 18, center_format)
        # 헤더 색,배경
        worksheet_access.conditional_format(st_row, 0, st_row, len(access_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': header_format})
        # 출력값
        worksheet_access.conditional_format(st_row, 0, ed_row, len(access_labels), {
            'type': 'cell',
            'criteria': 'not equal to',
            'value': '"XX"',
            'format': border_format})

        #print('workspace info : ', df_access)

        # saved the xlsx
        writer_vpc_info.save()

        with open(writer_vpc_info.path, 'rb') as f:
            # 슬렉 주석
            slack_client.api_call('chat.postMessage', channel=channel_id,
                                  text='변환 완료 -> {} slack 업로드'.format(xlsx_name))
            slack_client.api_call('files.upload', channels=channel_id, file=f, filename=xlsx_name)
            slack_client.api_call('chat.postMessage', channel=channel_id, text=':sadrabbit: 작업완료 :pika:')
    except TypeError:
        slack_client.api_call('chat.postMessage', channel=channel_id, text='입력하신 vpc가 존재하는지 확인해주세요.')

if __name__ == '__main__':
    print('Console to xlsx started')
    #lambda_handler([], [])