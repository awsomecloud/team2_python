class security_groups:
    def __init__(self, ec2_service, type):
        self.ec2_service = ec2_service
        self.type = type




    # name is vpc-id or group-id and value is vpc-id or group-id
    def describe_securities(self, name, value):
        response = self.ec2_service.describe_security_groups(
            Filters=[{
                'Name': name,
                'Values': [value]
            }]
        )

        return response['SecurityGroups']

    def descirbe_sg_ids(self, vpc_id):
        response = self.describe_securities('vpc-id', vpc_id)
        sg_group_ids = []
        for secid in response:
            for key, val in secid.items():
                if key == 'GroupId':
                    sg_group_ids.append(val)

        return sg_group_ids

    def get_ip_ranges(self, sg_id, group_name, ip_permitions, ip_permitions_num):
        protocol = ''
        protocol_type = ''
        port_range = ''
        sources = ''
        descrip = ''
        result = []

        if ip_permitions_num > 0:

            for permitions in ip_permitions:
                descrip = ''
                protocol = permitions['IpProtocol']

                if protocol == '-1':
                    port_range, protocol = 'ALL', 'ALL'
                    protocol_type = 'ALL Traffic'
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 80:
                    protocol_type = 'HTTP(80)'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 443:
                    protocol_type = 'HTTPS'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 389:
                    protocol_type = 'LDAP'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 465:
                    protocol_type = 'SMTPS'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 993:
                    protocol_type = 'IMAPS'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 1433:
                    protocol_type = 'MSSQL'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 2049:
                    protocol_type = 'NFS'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 3306:
                    protocol_type = 'MYSQL/Aurora'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 3389:
                    protocol_type = 'RDP'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 5439:
                    protocol_type = 'RedShift'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 5432:
                    protocol_type = 'PostgreSQL'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 1521:
                    protocol_type = 'ORACLE'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 110:
                    protocol_type = 'POP3'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 143:
                    protocol_type = 'IMAP'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 389:
                    protocol_type = 'LDAP'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 22:
                    protocol_type = 'SSH(22)'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] != 22 and permitions[
                    'FromPort'] != 80:
                    protocol_type = 'Custom TCP Rule'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'tcp' and permitions['FromPort'] == 0:
                    protocol_type = 'ALL TCP'
                    port_range = 'ALL'
                if 'FromPort' in permitions and permitions['FromPort'] != permitions['ToPort']:
                    port_range = str(permitions['FromPort']) + '-' + str(permitions['ToPort'])
                if 'FromPort' in permitions and protocol == 'udp' and permitions['FromPort'] != 0:
                    protocol_type = 'Custom UDP Rule'
                    port_range = permitions['ToPort']
                if 'FromPort' in permitions and protocol == 'udp' and permitions['FromPort'] == 0:
                    protocol_type = 'ALL UDP'
                    port_range = 'ALL'
                if protocol == 'icmp':
                    protocol_type = 'ALL ICMP - IPV4'
                    port_range = 'ALL'

                if permitions['IpRanges'] != []:
                    for j in permitions['IpRanges']:
                        if len(j) == 2:
                            sources = j['CidrIp']
                            descrip = j['Description']
                        if len(j) == 1:
                            sources = j['CidrIp']
                        if len(j) == 0:
                            sources = 'No source'
                        # if protocol != '' and port_range != '' and sources != '' and descrip != '':
                        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))
                        descrip = ' '

                if permitions['UserIdGroupPairs'] != []:
                    for i in permitions['UserIdGroupPairs']:
                        if len(i) == 3:
                            sources = i['GroupId']
                            descrip = i['Description']
                        if len(i) == 2:
                            sources = i['GroupId']
                        if len(i) == 0:
                            sources = 'No source'
                        # if protocol != '' and port_range != '' and sources != '' and descrip != '':
                        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))
                        descrip = ' '
                if permitions['PrefixListIds'] != []:
                    for i in permitions['PrefixListIds']:
                        sources = i['PrefixListId']
                        descrip = i['Description']
                        # if protocol != '' and port_range != '' and sources != '' and descrip != '':
                        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))
                        descrip = ' '
        else:
            result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))

        return result

    def get_ip_ranges2(self, sg_id, group_name):
        protocol = ''
        protocol_type = ''
        port_range = ''
        sources = ''
        descrip = ''
        result = []


        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))
        descrip = ' '

        return result

    # sg_ids is list type
    def describe_ips(self, vpc_id):
        result = []
        group_name = ''
        get_permissions = None
        sg_ids = self.descirbe_sg_ids(vpc_id)
        type = self.type

        #print("테스트를 해보겠습니다. : " + vpc_id)
        #print(sg_ids)

        for sg in sg_ids:
            sg_info = self.describe_securities('group-id', sg)

            for sg_list in sg_info:
                for gp_key, gp_val in sg_list.items():
                    if gp_key == 'GroupName':
                        group_name = gp_val
                    if type == 'in':
                        if gp_key == 'IpPermissions':
                            IpPermissions_num = len(gp_val)
                            get_permissions = self.get_ip_ranges(sg, group_name, gp_val, IpPermissions_num)
                    else:
                        if gp_key == 'IpPermissionsEgress':
                            IpPermissions_num = len(gp_val)
                            get_permissions = self.get_ip_ranges(sg, group_name, gp_val, IpPermissions_num)
                            # if get_permissions == []:
                            #     print('오류 체킹임' + type)
                            #     print(sg_info)
                            #     print('오류 체킹임 gpval')
                            #     print(gp_val)
                            #     print(IpPermissions_num)


            result.append(get_permissions)

        return result