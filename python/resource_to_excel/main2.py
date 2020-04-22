import pandas as pd
import boto3
from boto3.session import Session
import vpc_service, subnet_service, route_service, vpn_service, nat_service
import security_service, ec2_service, elb_service, rds_service, cloudfront_service
import alb_service, tg_service, vpc_peer_service
import s3_service, direct_connect_service, workspace_service, iam_service, efs_service, endpoint_service
from slackclient import SlackClient
import sys
import base64
import concurrent.futures
import time
from urllib import parse

# Gathering vpc infos, name, id, cidr, flow logs
def get_vpc_info(tag_val, ec2, check_type):
    print('get_vpc_info - start')
    vpc = vpc_service.vpc(ec2)
    get_vpc = vpc.desecribe_vpc(tag_val, check_type)

    finish = str(time.perf_counter())
    print('get_vpc_info - ' + finish)
    return get_vpc

# vpc_id is list type
def get_subnet_info(vpc_id, ec2):
    print('get_vpc_info - start')
    subnets = subnet_service.subnet(ec2)
    get_sub_info = subnets.describe_subnet(vpc_id)

    finish = str(time.perf_counter())
    print('get_subnet_info - ' + finish)
    return get_sub_info


# subnet_id is list type
def get_route_info(ec2, vpc_id):
    print('get_vpc_info - start')
    routes = route_service.route(ec2)
    get_route_info = routes.describe_route(vpc_id)

    finish = str(time.perf_counter())
    print('get_route_info - ' + finish)
    return get_route_info


# vpc_id is list type
def get_vpn_info(vpc_id, ec2):
    print('get_vpc_info - start')
    vpn = vpn_service.vpn(ec2)
    get_vpn_info = vpn.describe_vpn_gates(vpc_id)

    finish = str(time.perf_counter())
    print('get_vpn_info - ' + finish)
    return get_vpn_info


# vpc_id is list type
def get_nat_info(vpc_id, ec2):
    print('get_vpc_info - start')
    nat = nat_service.nat(ec2)
    get_nat_info = nat.describe_nats(vpc_id)

    finish = str(time.perf_counter())
    print('get_nat_info - ' + finish)
    return get_nat_info


def get_securities_info(vpc_id, ec2, type):
    print('get_vpc_info - start')
    securities = security_service.security_groups(ec2, type)
    get_securities_info = securities.describe_ips(vpc_id)

    finish = str(time.perf_counter())
    print('get_securities_info - ' + finish)
    return get_securities_info


def get_instances_info(vpc_id, ec2):
    print('get_vpc_info - start')
    instances = ec2_service.ec2(ec2)
    get_ec2_info = instances.get_instance_ids(vpc_id)

    finish = str(time.perf_counter())
    print('get_instances_info - ' + finish)
    return get_ec2_info


def get_elbs_info(elb):
    print('get_vpc_info - start')
    elbs = elb_service.elb(elb)
    get_classic_elb_info = elbs.descrbie_classic_elb()
    result = get_classic_elb_info

    finish = str(time.perf_counter())
    print('get_elbs_info - ' + finish)
    return result

#190516 alb 추가
def get_albs_info(vpc_id ,elbv2):
    print('get_vpc_info - start')
    albs =  alb_service.alb(vpc_id, elbv2) #elb_service 파일내의 alb class
    get_not_classic_elb_info = albs.describe_not_classic_elb()
    result = get_not_classic_elb_info

    finish = str(time.perf_counter())
    print('get_albs_info - ' + finish)
    return result

#190516 target group 추가
def get_tg_info(vpc_id, elbv2):
    print('get_vpc_info - start')
    tg = tg_service.tg(vpc_id, elbv2)
    get_target_group_info = tg.describe_target_groups()
    result = get_target_group_info

    finish = str(time.perf_counter())
    print('get_tg_info - ' + finish)
    return result


def get_rds_info(vpc_id, rds):
    print('get_vpc_info - start')
    rdss = rds_service.rds(vpc_id, rds)
    get_rds_info = rdss.get_db_arn()

    finish = str(time.perf_counter())
    print('get_rds_info - ' + finish)
    return get_rds_info


def get_cf_info(cf):
    print('get_vpc_info - start')
    cfs = cloudfront_service.cloudfront(cf)
    get_cfs_info = cfs.describe_cfs()

    finish = str(time.perf_counter())
    print('get_cf_info - ' + finish)
    return get_cfs_info


def get_s3_info(s3):
    print('get_vpc_info - start')
    s3s = s3_service.s3s(s3)
    get_s3s_info = s3s.describe_s3s()

    finish = str(time.perf_counter())
    print('get_s3_info - ' + finish)
    return get_s3s_info


def get_dx_info(direct):
    print('get_vpc_info - start')
    direct = direct_connect_service.direct_connect(direct)
    get_direct_connection = direct.describe_dx()

    finish = str(time.perf_counter())
    print('get_dx_info - ' + finish)
    return get_direct_connection

#190523 workspace 추가
def get_workspace_info(workspace, ec2, vpc_id):
    print('get_vpc_info - start')
    workspaces = workspace_service.ws(workspace, ec2, vpc_id)
    get_workspace_info = workspaces.describe_workspace_info()

    finish = str(time.perf_counter())
    print('get_workspace_info - ' + finish)
    return get_workspace_info

#190524 iam 추가
def get_iam_user_info(iam, access_yn):
    print('get_vpc_info - start')
    iam = iam_service.iam(iam, access_yn)
    get_iam_info = iam.describe_iam_user_info()

    finish = str(time.perf_counter())
    print('get_iam_user_info - ' + finish)
    return get_iam_info

#190603 efs 추가
def get_efs_info(efs, ec2, vpc_id, region_id):
    print('get_vpc_info - start')
    efs = efs_service.ef(efs, ec2, vpc_id, region_id)
    get_efs_info = efs.describe_efs_info()

    finish = str(time.perf_counter())
    print('get_efs_info - ' + finish)
    return get_efs_info

# 191022 vpc peering 추가
def get_vpc_peer_info(ec2):
    print('get_vpc_info - start')
    vpc = vpc_peer_service.vpc_peer(ec2)
    get_vpc_peer = vpc.desecribe_vpc_peer()

    finish = str(time.perf_counter())
    print('get_vpc_peer_info - ' + finish)
    return get_vpc_peer

#200221 iam role 추가
def get_iam_role_info(iam, access_yn):
    print('get_vpc_info - start')
    iam = iam_service.iam(iam, access_yn)
    get_iam_info = iam.describe_iam_role_info()

    finish = str(time.perf_counter())
    print('get_iam_user_info - ' + finish)
    return get_iam_info

#200221 iam group 추가
def get_iam_group_info(iam, access_yn):
    print('get_vpc_info - start')
    iam = iam_service.iam(iam, access_yn)
    get_iam_group_info = iam.describe_iam_group_info()

    finish = str(time.perf_counter())
    print('get_iam_group_info - ' + finish)
    return get_iam_group_info

#200304 endpoint 정보 추가
def get_endpoint_info(iam, vpc_id):
    print('get_endpoint_info - start')
    endpoint = endpoint_service.endpoint(iam, vpc_id)
    get_endpoint_info = endpoint.describe_endpoint_info()

    finish = str(time.perf_counter())
    print('get_endpoint_group_info - ' + finish)
    return get_endpoint_info



def lambda_handler(event, context):
    start = time.perf_counter()

    #data_parameters = event['text'].split(' ')
    # basic environment setting
    # profile_name = data_parameters[2]

    region = 'ap-northeast-2'
    access_key = ''
    secret_key = ''
    session_token = ''
    tag_val = ['']
    xlsx_name = '200323.xlsx'
    # basic environment setting

    # [민걸] session 추가 하였음 aws_access_key_id, aws_secret_access_key
    session = Session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    ec2 = session.client('ec2', region_name=region)
    direct_connect = session.client('directconnect', region_name=region)
    elb = session.client('elb', region_name=region)
    elbv2 = session.client('elbv2')
    rds = session.client('rds', region_name=region)
    cf = session.client('cloudfront')
    s3 = session.client('s3')
    direct = session.client('directconnect')
    workspace = session.client('workspaces')
    iam = session.client('iam')
    efs = session.client('efs')

    writer_vpc_info = pd.ExcelWriter(xlsx_name, engine='xlsxwriter')
    workbook = writer_vpc_info.book
    start_row = 3
    iam_start_row = 2

    #-----------------xlsx 디자인 용 -----------------------------
    # format to apply to xlsx
    all_format = workbook.add_format({
        'font_size': 10
    })
    # format to apply to xlsx
    border_format = workbook.add_format({
        'border': 1,
        'font_size': 10
    })
    # 최상위
    h_header_format = workbook.add_format({
        'align': 'left',
        'bold': 1,
        'font_size': 10
    })
    # 중앙정렬 format
    center_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    # 헤더 배경 + 글씨 format
    header_format = workbook.add_format({
        'font_color': 'white',
        'font_size': 10,
        'border': 1,
        'bold': 1,
        'bg_color': '#9d9d9d'
    })
    # A라인 bold 처리
    bold_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    print('t스레드 테스트')
    #스레드 화
    #vpc 는 스레드가 불가능 다른 function 에서 vpc id가 전부 필요함 솔직히 하...
    vpc_values = get_vpc_info(tag_val, ec2, 'tag')
    vpc_ids = []
    nat_values = None
    for name, vpc_id, _, _ in vpc_values:
        vpc_ids.append(vpc_id)

    vid = vpc_ids[0]

    #instances_values = get_instances_info(vid, ec2)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        #iam thread
        t_iam = executor.submit(get_iam_user_info, iam, 'n')
        # vpc thread
        # t_vpc = executor.submit(get_vpc_info, ec2, 'tag')
        # vpc_values = t_vpc.result()
        # subnet thread
        t_subnet = executor.submit(get_subnet_info, vpc_ids, ec2)

        # route thread
        t_route = executor.submit(get_route_info, ec2, vpc_ids)

        # nat thread
        t_nat = executor.submit(get_nat_info, vid, ec2)

        # endpoint thread

        # direct thread
        t_direct = executor.submit(get_dx_info, direct)

        # vpc_peer thread
        t_vpc_peer = executor.submit(get_vpc_peer_info, ec2)

        # vpn thread
        t_vpn = executor.submit(get_vpn_info, vid, ec2)

        # sg group inbound thread
        t_sg_in = executor.submit(get_securities_info, vid, ec2, 'in')

        # sg group outbound thread
        t_sg_out = executor.submit(get_securities_info, vid, ec2, 'out')

        # ec2 thread
        t_ec2 = executor.submit(get_instances_info, vid, ec2)

        # elb thread
        t_elb = executor.submit(get_elbs_info, elb)

        # alb thread
        t_alb = executor.submit(get_albs_info, vid, elbv2)

        # target gp thread
        t_tg = executor.submit(get_tg_info, vid, elbv2)

        # rds thread
        t_rds = executor.submit(get_rds_info, vid, rds)

        # cf thread
        t_cf = executor.submit(get_cf_info, cf)

        # s3 thread
        t_s3 = executor.submit(get_s3_info, s3)

        # workspace thread
        t_workspace = executor.submit(get_workspace_info, workspace, ec2, vid)

        # efs thread
        t_efs = executor.submit(get_efs_info, efs, ec2, vid, region)

        # access key thread
        t_a_key = executor.submit(get_iam_user_info, iam, 'y')

        #병렬 작업 시작
        instances_values = t_ec2.result()
        iam_values = t_iam.result()
        sub_values = t_subnet.result()
        route_values = t_route.result()
        nat_values = t_nat.result()
        direct_values = t_direct.result()
        vpc_peer_values = t_vpc_peer.result()
        vpn_values = t_vpn.result()
        security_values_in = t_sg_in.result()
        security_values_out = t_sg_out.result()
        elbs_values = t_elb.result()
        albs_values = t_alb.result()
        tg_values = t_tg.result()
        rds_values = t_rds.result()
        cfs_values = t_cf.result()
        s3_values = t_s3.result()
        workspace = t_workspace.result()
        efs_info = t_efs.result()
        access_info = t_a_key.result()


    print('t스레드 테스트 끝')
    # ----------------------------------------------------------
    # get iam info
    #iam_values = get_iam_info(iam, 'n')
    iam_labels = ['Account Number', '용도', 'AWS Management Console URL', 'ID', 'PW', 'Permission', '비고']
    df_iam = pd.DataFrame.from_records(iam_values, columns=iam_labels)
    df_iam.index += 1
    df_iam.to_excel(writer_vpc_info, sheet_name='3.AWS 접속정보', startrow=2)
    worksheet_iam = writer_vpc_info.sheets['3.AWS 접속정보']
    worksheet_iam.write(0, 0, '3.AWS 접속정보', h_header_format)
    worksheet_iam.write(iam_start_row, 0, '연번', center_format)

    st_row = 2
    ed_row = st_row + len(df_iam)

    # 포멧 설정
    #모든 사이즈 10 통일

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
# --------------------VPC 정보 Tab-----------------------------
    # get vpc info
    # tag_val = [sys.argv[1]]  # ['api_private_test']

    vpc_labels = ['Name', 'ID', 'CIDR', 'Flow Logs']
    #vpc_values = get_vpc_info(tag_val, ec2, 'tag')
    df_vpc = pd.DataFrame.from_records(vpc_values, columns=vpc_labels)
    df_vpc.index += 1
    df_vpc.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=3)

    worksheet = writer_vpc_info.sheets['4.VPC 구성정보']
    worksheet.write(0, 0, '2. VPC 구성정보', h_header_format)
    worksheet.write(2, 0, '2.1 VPC 현황', h_header_format)
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

    # get subnet info
    # vpc_ids = []
    # for name, vpc_id, _, _ in vpc_values:
    #     vpc_ids.append(vpc_id)

    subnet_labels = ['Name', 'ID', 'VPC', 'CIDR', 'Route Table']
    #sub_values = get_subnet_info(vpc_ids, ec2)
    df_subnet = pd.DataFrame.from_records(sub_values, columns=subnet_labels)
    df_subnet.index += 1
    df_subnet.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.2 Subnet 현황', h_header_format)
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

    route_labels = ['Name', 'Route Table ID', 'Main']
    #route_values = get_route_info(ec2, vpc_ids)
    df_route = pd.DataFrame.from_records(route_values, columns=route_labels)
    df_route.index += 1
    df_route.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.3 Route Table 현황', h_header_format)
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
    nat_labels = ['ID', 'EIP', 'PIP', 'VPC', 'Subnet']
    # for vid in vpc_ids:
    #     nat_values = get_nat_info(vid, ec2)
    df_nat = pd.DataFrame.from_records(nat_values, columns=nat_labels)
    df_nat.index += 1
    df_nat.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.5 NAT Gateway 현황', h_header_format)
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
    #direct_values = get_dx_info(direct)
    direct_labels = ['Name', 'ID', 'Connection', 'VGW', 'Your Peer IP', 'Amazon Peer IP']
    df_direct = pd.DataFrame.from_records(direct_values, columns=direct_labels)
    df_direct.index += 1
    df_direct.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.6 Direct Connect 현황', h_header_format)
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
    #vpc_peer_values = None
    vpc_peer_labels = ['Name', 'ID', 'Status', 'Requester VPC', 'Accepter VPC', 'Requester CIDR', 'Accepter CIDR',
                       'Requester VPC DNS', 'Accepter VPC DNS']

    #vpc_peer_values = get_vpc_peer_info(ec2)

    df_vpc_peer_labels = pd.DataFrame.from_records(vpc_peer_values, columns=vpc_peer_labels)
    df_vpc_peer_labels.index += 1
    df_vpc_peer_labels.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.7 VPC Peering 현황', h_header_format)
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
    #vpn_values = None
    vpn_labels = ['Name', 'CGW ID', 'VPN ID', 'Customer IP', 'id_asn', 'tunnel1', 'tunnel2', 'static_routes', 'etc']

    # for vid in vpc_ids:
    #     vpn_values = get_vpn_info(vid, ec2)
        # print('nat infoaaa :', vpn_values)
    df_vpn = pd.DataFrame.from_records(vpn_values, columns=vpn_labels)
    df_vpn.index += 1
    df_vpn.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.8 VPN 현황', h_header_format)
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
    #security_values = None
    df_sg = pd.DataFrame()
    sg_labels = ['ID', 'Name', 'Type', 'Protocol', 'Port Range', 'Source', 'Description']
    # for vid in vpc_ids:
    #     security_values_in = get_securities_info(vid, ec2, 'in')
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
    for col in security_values_in:
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
    worksheet.write(start_row - 1, 0, '2.9 Security Group 현황(InBound)', h_header_format)
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
    #security_values = None
    df_sg = pd.DataFrame()
    sg_labels = ['ID', 'Name', 'Type', 'Protocol', 'Port Range', 'Destination', 'Description']
    # for vid in vpc_ids:
    #     security_values_out = get_securities_info(vid, ec2, 'out')
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
    for col in security_values_out:
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
    worksheet.write(start_row - 1, 0, '2.10 Security Group 현황(OutBound)', h_header_format)
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



#--------------------인스턴스 정보 Tab-----------------------------
    # get instance info
    #instances_values = None
    ec2_start_row = 3
    df_ec2 = pd.DataFrame()
    ec2_labels = ['Name', 'Instance ID', 'Type', 'AZ', 'Key Pair', 'Security Group', 'IAM Role', 'EIP', 'PIP', 'ID',
                  'PW', 'EBS', 'OS', 'etc', 'UserData']

    # for vid in vpc_ids:
    #     instances_values = get_instances_info(vid, ec2)

    ec2_to_append = pd.DataFrame.from_records(instances_values, columns=ec2_labels)
    df_ec2 = df_ec2.append(ec2_to_append)
    df_ec2.index += 1
    df_ec2.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=3)
    worksheet_ec2 = writer_vpc_info.sheets['5.EC2 현황정보']
    worksheet_ec2.write(0, 0, '3. EC2 현황정보', h_header_format)
    worksheet_ec2.write(2, 0, '3.1 Instance 현황', h_header_format)
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
    #elbs_values = get_elbs_info(elb)
    elb_labels = ['Name', 'DNS Name', 'Port', 'AZ', 'Host Count', 'Health Check']
    df_elbs = pd.DataFrame.from_records(elbs_values, columns=elb_labels)
    df_elbs.index += 1
    df_elbs.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
    worksheet_ec2.write(ec2_start_row - 1, 0, '3.2 ELB 현황', h_header_format)
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

    # for vid in vpc_ids:
    #     albs_values = get_albs_info(vid, elbv2)
    df_albs = pd.DataFrame.from_records(albs_values, columns=alb_labels)
    df_albs.index += 1
    df_albs.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
    worksheet_ec2.write(ec2_start_row - 1, 0, '3.3 ALB 현황', h_header_format)
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
    # for vid in vpc_ids:
    #     tg_values = get_tg_info(vid, elbv2)
    tg_labels = ['Name', 'Port', 'Health Protocol', 'Health Intervalseconds', 'Health timeoutseconds',
                 'Health ThresholdCount', 'UnHealth ThresholdCount', 'Health path', 'used alb']
    df_tg = pd.DataFrame.from_records(tg_values, columns=tg_labels)
    df_tg.index += 1
    df_tg.to_excel(writer_vpc_info, sheet_name='5.EC2 현황정보', startrow=ec2_start_row)
    worksheet_ec2.write(ec2_start_row - 1, 0, '3.4 Target Group 현황', h_header_format)
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
    # for vid in vpc_ids:
    #     rds_values = get_rds_info(vid, rds)
    rds_labels = ['Name', 'DB Name', 'DB Engine', 'Type', 'Storage', 'ID', 'PW', 'Character Set', 'Multi-Az',
                  'Publicly', 'Endpoint', 'Security Groups', 'Subnet Group', 'Parameters / Option Groups']
    df_rds = pd.DataFrame.from_records(rds_values, columns=rds_labels)
    df_rds.index += 1
    df_rds.to_excel(writer_vpc_info, sheet_name='6.RDS 현황정보', startrow=2)
    worksheet_rds = writer_vpc_info.sheets['6.RDS 현황정보']
    worksheet_rds.write(0, 0, '4.RDS 현황정보', h_header_format)
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
    #cfs_values = get_cf_info(cf)
    cfs_labels = ['ID', 'Domain', 'Origin', 'CNAMEs', 'Etc']
    cf_start_row = 3
    df_cfs = pd.DataFrame.from_records(cfs_values, columns=cfs_labels)
    df_cfs.index += 1
    df_cfs.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
    worksheet_cf = writer_vpc_info.sheets['7.CloudFront&S3']
    worksheet_cf.write(0, 0, 'CloudFront&S3 현황정보', h_header_format)
    worksheet_cf.write(2, 0, '5.1CloudFront', h_header_format)
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
    #s3_values = get_s3_info(s3)
    s3_labels = ['Bucket Name', 'Region', 'Use', 'User', 'Authority']
    df_s3s = pd.DataFrame.from_records(s3_values, columns=s3_labels)
    df_s3s.index += 1
    df_s3s.to_excel(writer_vpc_info, sheet_name='7.CloudFront&S3', startrow=cf_start_row)
    worksheet_cf.write(cf_start_row - 1, 0, '5.S3', h_header_format)
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
    # for vid in vpc_ids:
    #     workspace = get_workspace_info(workspace, ec2, vid)
    ws_labels = ['WorkSpace ID', 'Username', 'Compute', 'Running Mode', 'Root Volume', 'User Volume', 'Status']
    df_ws = pd.DataFrame.from_records(workspace, columns=ws_labels)
    df_ws.index += 1
    df_ws.to_excel(writer_vpc_info, sheet_name='8.Workspace 현황정보', startrow=2)
    worksheet_ws = writer_vpc_info.sheets['8.Workspace 현황정보']
    worksheet_ws.write(0, 0, '8.Workspace 현황정보', h_header_format)
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
    # for vid in vpc_ids:
    #     efs_info = get_efs_info(efs, ec2, vid, region)
    efs_labels = ['Name', 'ID', 'Size', 'Performance Mode', 'Mount Info', 'DNS', 'Security Groups']
    df_efs = pd.DataFrame.from_records(efs_info, columns=efs_labels)
    df_efs.index += 1
    df_efs.to_excel(writer_vpc_info, sheet_name='8.EFS 현황정보', startrow=2)
    worksheet_efs = writer_vpc_info.sheets['8.EFS 현황정보']
    worksheet_efs.write(0, 0, '8.EFS 현황정보', h_header_format)
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

    # get accessKey info
    # access_info = get_iam_info(iam, 'y')
    access_labels = ['ID', 'Access Key', 'Secret Access Key', 'Permission', '비고']
    df_access = pd.DataFrame.from_records(access_info, columns=access_labels)
    df_access.index += 1
    df_access.to_excel(writer_vpc_info, sheet_name='9.AccessKey', startrow=2)
    worksheet_access = writer_vpc_info.sheets['9.AccessKey']
    worksheet_access.write(0, 0, '9.AccessKey', h_header_format)
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

    #print('---------file path------------')
    #print(writer_vpc_info.path)
    f = open(writer_vpc_info.path, 'rb')
    file_content = f.read()

    outputbase64 = str(base64.b64encode(file_content).decode('utf-8'))

    finish = time.perf_counter()
    print(finish)
    print(f'Finished in {round(finish - start, 2)} second(s)')

    test05 = {'statusCode': 200,
              'body': outputbase64,
              'headers':
                  {'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                   'Content-Disposition': 'attachment; filename=\"hello.xlsx\"'},
              'isBase64Encoded': True
              }


    return test05
    '''
    with open(writer_vpc_info.path, 'rb') as f:
        s3.put_object(
            Body=f,
            Bucket='transcoder-test-input-seoul',
            Key=xlsx_name
        )
    '''


if __name__ == '__main__':
    print('Console to xlsx started')

    lambda_handler([], [])