import pandas as pd
import pandas.io.formats.excel
pandas.io.formats.excel.header_style = None
import boto3
from boto3.session import Session
import vpc_service, subnet_service, route_service, vpn_service, nat_service
import security_service, ec2_service, elb_service, rds_service, cloudfront_service
import alb_service, tg_service, vpc_peer_service, sg_in_out_chack_service, transit_gateway_service
import s3_service, direct_connect_service, workspace_service, iam_service, efs_service, endpoint_service, cloudwatch_service, lambda_service, glue_service
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
    get_direct_connection = direct.describe_main()

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
def get_endpoint_info(ec2, vpc_id):
    print('get_endpoint_info - start')
    endpoint = endpoint_service.endpoint(ec2, vpc_id)
    get_endpoint_info = endpoint.describe_endpoint_info()

    finish = str(time.perf_counter())
    print('get_endpoint_group_info - ' + finish)
    return get_endpoint_info

#200304 cloudevent 정보 추가
def get_cloudwatch_info(cw):
    print('get_cloudwatch_info - start')
    cloudwatch_event = cloudwatch_service.cw(cw)
    get_cloudwatch_info = cloudwatch_event.describe_cw()

    finish = str(time.perf_counter())
    print('get_cloudwatch_group_info - ' + finish)
    return get_cloudwatch_info

#200313 cloudevent 정보 추가
def get_lambda_info(lamb):
    print('get_lambda_info - start')
    lambda_event = lambda_service.c_lambda(lamb)
    get_lambda_info = lambda_event.describe_lambda_info()

    finish = str(time.perf_counter())
    print('get_lambda_info - ' + finish)
    return get_lambda_info

#200313 glue 정보 추가
def get_glue_info(glue, type):
    print('get_glue_info - start')
    glue_event = glue_service.glue(glue, type)
    get_glue_info = glue_event.describe_glue_info()

    finish = str(time.perf_counter())
    print('get_lambda_info - ' + finish)
    return get_glue_info

#200316 sg inout check 정보 추가
def get_sginout_info(glue, type):
    print('get_sginout_info - start')
    glue_event = sg_in_out_chack_service.glue(glue, type)
    get_glue_info = glue_event.describe_glue_info()

    finish = str(time.perf_counter())
    print('get_sginout_info - ' + finish)
    return get_glue_info

#200327 Transit Gateway 정보 추가
def get_tsg_info(tsg):
    print('get_vpc_info - start')
    transit_gateway = transit_gateway_service.transit_gateway(tsg)
    get_transit_info = transit_gateway.describe_main()

    finish = str(time.perf_counter())
    print('get_dx_info - ' + finish)
    return get_transit_info

def set_excel_info(first_type, label, value, sheet_name, n_sheet_name,excel_info, worksheet, start_row):
    workbook = excel_info.book
    # -----------------xlsx 디자인 용 -----------------------------
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
        'bold': 1,
        'align': 'left',
        'font_size': 10
    })
    # 중앙정렬 format
    center_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'text_wrap': True
    })
    # 헤더 배경 + 글씨 format
    header_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'font_size': 10,
        'bg_color': '#9d9d9d'
    })
    # A라인 bold 처리
    bold_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })

    #-----------excel_set--------------
    df_info = pd.DataFrame.from_records(value, columns=label)
    df_info.index += 1
    df_info.to_excel(excel_info, sheet_name=sheet_name, startrow=start_row)
    if first_type:
        worksheet = excel_info.sheets[sheet_name]
        worksheet.write(0, 0, sheet_name, h_header_format)
    worksheet.write(start_row - 1, 0, n_sheet_name, h_header_format)
    worksheet.write(start_row, 0, '연번')

    st_row = start_row
    ed_row = st_row + len(df_info)

    # 포멧 설정
    # A라인 bold 처리
    worksheet.set_column('A:A', 18, bold_format)
    # 중앙 정렬
    worksheet.set_column('B:P', 18, center_format)
    # 헤더 색,배경
    worksheet.conditional_format(st_row, 0, st_row, len(label), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet.conditional_format(st_row, 0, ed_row, len(label), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    start_row += len(df_info) + 3

    return worksheet, start_row


def lambda_handler(event, context):
    start = time.perf_counter()

    #data_parameters = event['text'].split(' ')
    # basic environment setting
    # profile_name = data_parameters[2]

    region = 'ap-northeast-2'
    access_key = ''
    secret_key = ''
    session_token = ''
    tag_val = ['poc-mingeol-vpc']
    xlsx_name = 'poc-mingeol-vpc-200402.xlsx'


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
    cw = session.client('events')
    lamb = session.client('lambda')
    glue = session.client('glue')

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
        'bold': 1,
        'align': 'left',
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
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'font_size': 10,
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
        t_endpoint = executor.submit(get_endpoint_info, ec2, vid)

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

        # cloudwatch thread
        t_cloudwatch = executor.submit(get_cloudwatch_info, cw)

        # lambda thread
        t_lambda = executor.submit(get_lambda_info, lamb)

        #glue database thread
        t_glue_database = executor.submit(get_glue_info, glue, 0)

        #iam role, group thread
        t_iam_role = executor.submit(get_iam_role_info, iam, 'n')
        t_iam_group = executor.submit(get_iam_group_info, iam, 'n')

        #transit Gateway therad
        #t_tsg = executor.submit(get_tsg_info, ec2)

        # glue job thread
        #t_glue_job = executor.submit(get_glue_info, glue, 1)

        # glue triger thread
        #t_glue_tri = executor.submit(get_glue_info, glue, 2)

        #병렬 작업 시작
        instances_values = t_ec2.result()
        iam_values = t_iam.result()
        sub_values = t_subnet.result()
        route_values = t_route.result()
        nat_values = t_nat.result()
        dx_conn_result, dx_vi_result, dx_gate_result, dx_vi_attach_result, dx_gate_assoc_result = t_direct.result()
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
        endpoint_info = t_endpoint.result()
        cloudwatch_info = t_cloudwatch.result()
        lambda_info = t_lambda.result()
        glue_database_info = t_glue_database.result()
        iam_group_info = t_iam_group.result()
        iam_role_info = t_iam_role.result()
        #transit_gateway_info = t_tsg.result()
        #glue_job_info = t_glue_job.result()
        #glue_tri_info = t_glue_tri.result()


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

    # get endpoint info
    endpoint_labels = ['Name', 'ID', 'VPC ID', 'Endpoint type', 'Service name', '비고']
    # for vid in vpc_ids:
    #     nat_values = get_nat_info(vid, ec2)
    df_endpoint = pd.DataFrame.from_records(endpoint_info, columns=endpoint_labels)
    df_endpoint.index += 1
    df_endpoint.to_excel(writer_vpc_info, sheet_name='4.VPC 구성정보', startrow=start_row)
    worksheet.write(start_row - 1, 0, '2.5 EndPoint 현황', h_header_format)
    worksheet.write(start_row, 0, '연번')

    st_row = start_row
    ed_row = st_row + len(df_endpoint)

    # 포멧 설정
    # 중앙 정렬
    # worksheet.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet.conditional_format(st_row, 0, st_row, len(endpoint_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # vpc 출력값
    worksheet.conditional_format(st_row, 0, ed_row, len(endpoint_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    start_row += len(df_endpoint) + 3
    # print('nat info', df_nat)

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

    # --------------------new version start-----------------------------
    # get DX conn info
    #dx_conn_result, dx_vi_result, dx_gate_result, dx_vi_attach_result, dx_gate_assoc_result
    dx_start_row = 3
    dx_conn_labels = ['Name', 'ID', 'Region', 'location', '대역폭', '상태']
    worksheet_dx, dx_start_row = set_excel_info(True, dx_conn_labels, dx_conn_result, '5.DirectConnect 구성정보', '5.1 Connection 현황', writer_vpc_info, '', dx_start_row)

    # get DX vi info
    dx_vi_labels = ['Name', 'ID', 'Region', 'Connection ID', 'VLAN', '유형', '상태']
    worksheet_dx, dx_start_row = set_excel_info(False, dx_vi_labels, dx_vi_result, '5.DirectConnect 구성정보', '5.2 Virtual interface 현황', writer_vpc_info, worksheet_dx, dx_start_row)

    # get DX gate info
    dx_gate_labels = ['Name', 'ID', 'AWS 계정', 'Amazon ASN', '상태']
    worksheet_dx, dx_start_row = set_excel_info(False, dx_gate_labels, dx_gate_result, '5.DirectConnect 구성정보', '5.3 Direct Connect gateways 현황', writer_vpc_info, worksheet_dx, dx_start_row)

    # get DX vi_attach info
    dx_vi_attach_labels = ['Gateway Name', 'Gateway ID', 'Virtual interface ID', 'Region', 'AWS 계정', '유형', '상태']
    worksheet_dx, dx_start_row = set_excel_info(False, dx_vi_attach_labels, dx_vi_attach_result, '5.DirectConnect 구성정보', '5.4 Virtual interface attachments 현황', writer_vpc_info, worksheet_dx, dx_start_row)

    # get DX gate assoc info
    dx_gate_assoc_labels = ['Gateway Name', 'Gateway ID', 'Association ID', 'Region', 'AWS 계정', 'Allowed prefixes', '유형', '상태']
    worksheet_dx, dx_start_row = set_excel_info(False, dx_gate_assoc_labels, dx_gate_assoc_result, '5.DirectConnect 구성정보', '5.5 Gateway associations 현황', writer_vpc_info, worksheet_dx, dx_start_row)


    # get Transit GateWay info
    # dx_conn_result, dx_vi_result, dx_gate_result, dx_vi_attach_result, dx_gate_assoc_result
    # tsg_start_row = 3
    # tsg_conn_labels = ['Name', 'ID', 'Owner ID', 'State']
    # worksheet_tsg, dx_start_tsg = set_excel_info(True, tsg_conn_labels, tsg_result, '6.Transit GateWay 구성정보',
    #                                             '6.1 Transit Gateway 현황', writer_vpc_info, '', tsg_start_row)
    # --------------------new version end-----------------------------

    # get securties info
    #security_values = None
    df_sg = pd.DataFrame()
    sg_start_row = 3
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

    col_index = sg_start_row + 2
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
    df_sg.to_excel(writer_vpc_info, sheet_name='5.Security Group', startrow=sg_start_row)
    worksheet_sg = writer_vpc_info.sheets['5.Security Group']
    worksheet_sg.write(0, 0, '5.Security Group', h_header_format)
    worksheet_sg.write(2, 0, '5.1 Security Group 현황(InBound)', h_header_format)
    worksheet_sg.write(sg_start_row, 0, '연번')

    st_row = sg_start_row
    ed_row = st_row + len(df_sg)

    # 포멧 설정
    # 중앙 정렬
    worksheet_sg.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet_sg.conditional_format(st_row, 0, st_row, len(sg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_sg.conditional_format(st_row, 0, ed_row, len(sg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    sg_start_row += len(df_sg) + 3
    # print(df_sg)

    number_sg = 1
    for index in sg_merge_list:
        # print(index)
        if (index[1] - index[0]) == 0:
            worksheet_sg.write(index[0] - 1, 0, str(number_sg), bold_format)
            worksheet_sg.write(index[0] - 1, 1, index[2], center_format)
            worksheet_sg.write(index[0] - 1, 2, index[3], center_format)
        else:
            worksheet_sg.merge_range('A' + str(index[0]) + ':A' + str(index[1]), str(number_sg), bold_format)
            worksheet_sg.merge_range('B' + str(index[0]) + ':B' + str(index[1]), index[2], center_format)
            worksheet_sg.merge_range('C' + str(index[0]) + ':C' + str(index[1]), index[3], center_format)

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

    col_index = sg_start_row + 2
    #잠시 주석처리 여기 아래로
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
    df_sg.to_excel(writer_vpc_info, sheet_name='5.Security Group', startrow=sg_start_row)
    worksheet_sg.write(sg_start_row - 1, 0, '5.2 Security Group 현황(OutBound)', h_header_format)
    worksheet_sg.write(sg_start_row, 0, '연번')

    st_row = sg_start_row
    ed_row = st_row + len(df_sg)

    # 포멧 설정
    # 중앙 정렬
    # worksheet.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet_sg.conditional_format(st_row, 0, st_row, len(sg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_sg.conditional_format(st_row, 0, ed_row, len(sg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    sg_start_row += len(df_sg) + 3

    number_sg = 1
    for index in sg_merge_list:
        # print(index)
        if (index[1] - index[0]) == 0:
            worksheet_sg.write(index[0] - 1, 0, str(number_sg), bold_format)
            worksheet_sg.write(index[0] - 1, 1, index[2], center_format)
            worksheet_sg.write(index[0] - 1, 2, index[3], center_format)
        else:
            worksheet_sg.merge_range('A' + str(index[0]) + ':A' + str(index[1]), str(number_sg), bold_format)
            worksheet_sg.merge_range('B' + str(index[0]) + ':B' + str(index[1]), index[2], center_format)
            worksheet_sg.merge_range('C' + str(index[0]) + ':C' + str(index[1]), index[3], center_format)

        number_sg += 1

        # get sg_in_out_check info
        # sginout_labels = ['region', 'Group-Name', 'Group-ID', 'type', 'Port', 'Source/Destination', 'connection', 'ErrorInfo']
        # df_sginout = pd.DataFrame.from_records(access_info, columns=sginout_labels)
        # df_sginout.index += 1
        # df_sginout.to_excel(writer_vpc_info, sheet_name='9.SG group in out check', startrow=2)
        # worksheet_sginout = writer_vpc_info.sheets['9.AccessKey']
        # worksheet_sginout.write(0, 0, '9.AccessKey', h_header_format)
        # worksheet_sginout.write(2, 0, '연번')
        #
        # st_row = 2
        # ed_row = st_row + len(df_sginout)
        #
        # # 포멧 설정
        # # A라인 bold 처리
        # worksheet_sginout.set_column('A:A', 18, bold_format)
        # # 중앙 정렬
        # worksheet_sginout.set_column('B:H', 18, center_format)
        # # 헤더 색,배경
        # worksheet_sginout.conditional_format(st_row, 0, st_row, len(sginout_labels), {
        #     'type': 'cell',
        #     'criteria': 'not equal to',
        #     'value': '"XX"',
        #     'format': header_format})
        # # 출력값
        # worksheet_sginout.conditional_format(st_row, 0, ed_row, len(sginout_labels), {
        #     'type': 'cell',
        #     'criteria': 'not equal to',
        #     'value': '"XX"',
        #     'format': border_format})


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
    df_ec2.to_excel(writer_vpc_info, sheet_name='6.EC2 현황정보', startrow=3)
    worksheet_ec2 = writer_vpc_info.sheets['6.EC2 현황정보']
    worksheet_ec2.write(0, 0, '6. EC2 현황정보', h_header_format)
    worksheet_ec2.write(2, 0, '6.1 Instance 현황', h_header_format)
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

    # --------------------ELB 정보 Tab-----------------------------
    # get elb info
    # instances_values = None
    elb_start_row = 3
    elb_labels = ['Name', 'DNS Name', 'Port', 'AZ', 'Host Count', 'Health Check']

    df_elbs = pd.DataFrame.from_records(elbs_values, columns=elb_labels)
    df_elbs.index += 1
    df_elbs.to_excel(writer_vpc_info, sheet_name='7.ELB 현황정보', startrow=3)
    worksheet_elb = writer_vpc_info.sheets['7.ELB 현황정보']
    worksheet_elb.write(0, 0, '7.ELB 현황정보', h_header_format)
    worksheet_elb.write(elb_start_row - 1, 0, '7.1 ELB 현황', h_header_format)
    worksheet_elb.write(elb_start_row, 0, '연번')

    st_row = elb_start_row
    ed_row = st_row + len(df_elbs)

    # 포멧 설정
    # A라인 bold 처리
    worksheet_elb.set_column('A:A', 18, bold_format)
    # 중앙 정렬
    worksheet_elb.set_column('B:P', 18, center_format)
    # 헤더 색,배경
    worksheet_elb.conditional_format(st_row, 0, st_row, len(elb_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_elb.conditional_format(st_row, 0, ed_row, len(elb_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    elb_start_row += len(df_elbs) + 3

    # get albs info
    alb_labels = ['Name', 'DNS Name', 'ELB Type', 'AZ', 'Host Count']

    # for vid in vpc_ids:
    #     albs_values = get_albs_info(vid, elbv2)
    df_albs = pd.DataFrame.from_records(albs_values, columns=alb_labels)
    df_albs.index += 1
    df_albs.to_excel(writer_vpc_info, sheet_name='7.ELB 현황정보', startrow=elb_start_row)
    worksheet_elb.write(elb_start_row - 1, 0, '7.2 ALB 현황', h_header_format)
    worksheet_elb.write(elb_start_row, 0, '연번')

    st_row = elb_start_row
    ed_row = st_row + len(df_albs)

    # 포멧 설정
    # 중앙 정렬
    # worksheet.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet_elb.conditional_format(st_row, 0, st_row, len(alb_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_elb.conditional_format(st_row, 0, ed_row, len(alb_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    elb_start_row += len(df_albs) + 3

    #target group 정보
    tg_labels = ['Name', 'Port', 'Health Protocol', 'Health Intervalseconds', 'Health timeoutseconds',
                 'Health ThresholdCount', 'UnHealth ThresholdCount', 'Health path', 'used alb']
    df_tg = pd.DataFrame.from_records(tg_values, columns=tg_labels)
    df_tg.index += 1
    df_tg.to_excel(writer_vpc_info, sheet_name='7.ELB 현황정보', startrow=elb_start_row)
    worksheet_elb.write(elb_start_row - 1, 0, '7.3 Target Group 현황', h_header_format)
    worksheet_elb.write(elb_start_row, 0, '연번')

    st_row = elb_start_row
    ed_row = st_row + len(df_tg)

    # 포멧 설정
    # 중앙 정렬
    # worksheet.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet_elb.conditional_format(st_row, 0, st_row, len(tg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_elb.conditional_format(st_row, 0, ed_row, len(tg_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    # print('Target Group info ', df_tg)

    # get rds info
    # for vid in vpc_ids:
    #     rds_values = get_rds_info(vid, rds)
    #rds_labels = ['항목', '내용', '비고']
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
    s3_labels = ['Bucket Name', 'Region', 'Lifecycle Name', 'Transition Class', 'Transition at', 'Expire']
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

    # get cloudwatch info
    # cfs_values = get_cf_info(cf)
    cloudwatch_labels = ['CloudWatch Event Rules Name', 'Description', 'Schedule Cron expression', 'Targets ', 'Configure input']
    cw_start_row = 3
    df_cw = pd.DataFrame.from_records(cloudwatch_info, columns=cloudwatch_labels)
    df_cw.index += 1
    df_cw.to_excel(writer_vpc_info, sheet_name='8.CloudWatch&Lambda', startrow=cw_start_row)
    worksheet_cw = writer_vpc_info.sheets['8.CloudWatch&Lambda']
    worksheet_cw.write(0, 0, 'CloudFront&S3 현황정보', h_header_format)
    worksheet_cw.write(2, 0, '8.1 CloudWatch Event', h_header_format)
    worksheet_cw.write(3, 0, '연번')

    st_row = cw_start_row
    ed_row = st_row + len(df_cw)

    # 포멧 설정
    # A라인 bold 처리
    worksheet_cw.set_column('A:A', 18, bold_format)
    # 중앙 정렬
    worksheet_cw.set_column('B:F', 18, center_format)
    # 헤더 색,배경
    worksheet_cw.conditional_format(st_row, 0, st_row, len(cfs_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_cw.conditional_format(st_row, 0, ed_row, len(cfs_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})

    cw_start_row += len(df_cw) + 3

    # get s3 info
    # s3_values = get_s3_info(s3)
    lambda_labels = ['Lambda Function Name', 'Description', 'Runtime', 'handler name', '가동 제한시간', '비고']
    df_ld = pd.DataFrame.from_records(lambda_info, columns=lambda_labels)
    df_ld.index += 1
    df_ld.to_excel(writer_vpc_info, sheet_name='8.CloudWatch&Lambda', startrow=cw_start_row)
    worksheet_cw.write(cw_start_row - 1, 0, '8.2 Lambda', h_header_format)
    worksheet_cw.write(cw_start_row, 0, '연번')

    st_row = cw_start_row
    ed_row = st_row + len(df_ld)

    # 포멧 설정
    # 중앙 정렬
    # worksheet.set_column('A:Z', 18, center_format)
    # 헤더 색,배경
    worksheet_cw.conditional_format(st_row, 0, st_row, len(lambda_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': header_format})
    # 출력값
    worksheet_cw.conditional_format(st_row, 0, ed_row, len(lambda_labels), {
        'type': 'cell',
        'criteria': 'not equal to',
        'value': '"XX"',
        'format': border_format})


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

    # get DX conn info
    #iam_group_info iam_role_info
    iam_role_start_row = 3
    iam_role_labels = ['Role Name', 'Policy Name', '비고']
    worksheet_iam_role, iam_role_start_row = set_excel_info(True, iam_role_labels, iam_role_info, '9.IAM 구성정보', '5.1 IAM Role 현황', writer_vpc_info, '', iam_role_start_row)

    # get iam group info
    iam_group_labels = ['Group Name', 'Policy Name', '비고']
    worksheet_iam_role, iam_role_start_row = set_excel_info(False, iam_group_labels, iam_group_info, '9.IAM 구성정보', '5.2 IAM Group 현황', writer_vpc_info, worksheet_iam_role, iam_role_start_row)

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


    # get glue data base info
    # glue_database_labels = ['Database Name', 'Table Name', '위치', '분류', 'Connection name', 'Type']
    # glue_start_row = 3
    # df_glue_database = pd.DataFrame.from_records(glue_database_info, columns=glue_database_labels)
    # df_glue_database.index += 1
    # df_glue_database.to_excel(writer_vpc_info, sheet_name='13.glue', startrow=glue_start_row)
    # worksheet_glue = writer_vpc_info.sheets['13.glue']
    # worksheet_glue.write(0, 0, '13.glue', h_header_format)
    # worksheet_glue.write(2, 0, '연번')
    #
    # st_row = glue_start_row
    # ed_row = st_row + len(df_glue_database)
    #
    # # 포멧 설정
    # # A라인 bold 처리
    # worksheet_glue.set_column('A:A', 18, bold_format)
    # # 중앙 정렬
    # worksheet_glue.set_column('B:H', 18, center_format)
    # # 헤더 색,배경
    # worksheet_glue.conditional_format(st_row, 0, st_row, len(glue_database_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': header_format})
    # # 출력값
    # worksheet_glue.conditional_format(st_row, 0, ed_row, len(glue_database_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': border_format})
    #
    # glue_start_row += len(df_glue_database) + 3
    #
    # # get glue job info
    # glue_job_labels = ['Name', 'Type', 'ETL 언어', 'Script 위치']
    # df_glue_job = pd.DataFrame.from_records(glue_job_info, columns=glue_job_labels)
    # df_glue_job.index += 1
    # df_glue_job.to_excel(writer_vpc_info, sheet_name='13.glue', startrow=glue_start_row)
    # worksheet_glue.write(glue_start_row - 1, 0, '13.2 Glue Job', h_header_format)
    # worksheet_glue.write(glue_start_row, 0, '연번')
    #
    # st_row = glue_start_row
    # ed_row = st_row + len(df_glue_job)
    #
    # # 포멧 설정
    # # 중앙 정렬
    # # worksheet.set_column('A:Z', 18, center_format)
    # # 헤더 색,배경
    # worksheet_glue.conditional_format(st_row, 0, st_row, len(glue_job_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': header_format})
    # # 출력값
    # worksheet_glue.conditional_format(st_row, 0, ed_row, len(glue_job_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': border_format})


    # # get glue triger info
    # glue_tri_labels = ['Name', 'Type', 'Status', 'Parameter', '작업']
    # df_glue_tri = pd.DataFrame.from_records(glue_tri_info, columns=glue_tri_labels)
    # df_glue_tri.index += 1
    # df_glue_tri.to_excel(writer_vpc_info, sheet_name='13.glue', startrow=glue_start_row)
    # worksheet_glue.write(glue_start_row - 1, 0, '13.2 Glue Triger', h_header_format)
    # worksheet_glue.write(glue_start_row, 0, '연번')
    #
    # st_row = glue_start_row
    # ed_row = st_row + len(df_glue_tri)
    #
    # # 포멧 설정
    # # 중앙 정렬
    # # worksheet.set_column('A:Z', 18, center_format)
    # # 헤더 색,배경
    # worksheet_glue.conditional_format(st_row, 0, st_row, len(glue_tri_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': header_format})
    # # 출력값
    # worksheet_glue.conditional_format(st_row, 0, ed_row, len(glue_tri_labels), {
    #     'type': 'cell',
    #     'criteria': 'not equal to',
    #     'value': '"XX"',
    #     'format': border_format})

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