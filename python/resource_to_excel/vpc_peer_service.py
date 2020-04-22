class vpc_peer:

    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    def desecribe_vpc_peer(self):
        vpc_peer_result = []
        response = self.ec2_service.describe_vpc_peering_connections()
        for vpc_peer_info in response['VpcPeeringConnections'] :
            request_vpc_id = ''
            accept_vpc_id = ''
            request_cidr = ''
            accept_cidr = ''
            status = ''
            vpc_peer_id = ''
            vpc_peer_tag = ''
            request_vpc_dns = ''
            accept_vpc_dns = ''
            print(vpc_peer_info)
            accept_cidr = vpc_peer_info['AccepterVpcInfo']['CidrBlock']
            request_cidr = vpc_peer_info['RequesterVpcInfo']['CidrBlock']
            accept_vpc_id = vpc_peer_info['AccepterVpcInfo']['VpcId']
            request_vpc_id = vpc_peer_info['RequesterVpcInfo']['VpcId']
            status = vpc_peer_info['Status']['Code']
            vpc_peer_id = vpc_peer_info['VpcPeeringConnectionId']
            try:
                vpc_peer_tag = vpc_peer_info['Tags'][0]['Value']
            except IndexError:
                vpc_peer_tag = 'NULL'

            try:
                accept_vpc_dns = vpc_peer_info['AccepterVpcInfo']['PeeringOptions']['AllowDnsResolutionFromRemoteVpc']
            except KeyError:
                accept_vpc_dns = 'NULL'
            try:
                request_vpc_dns = vpc_peer_info['RequesterVpcInfo']['PeeringOptions']['AllowDnsResolutionFromRemoteVpc']
            except KeyError:
                request_vpc_dns = 'NULL'


            vpc_peer_result.append((vpc_peer_tag, vpc_peer_id, status, request_vpc_id, accept_vpc_id, request_cidr, accept_cidr, request_vpc_dns, accept_vpc_dns))

        print(vpc_peer_result)
        return vpc_peer_result