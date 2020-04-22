class nat:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    def describe_nats(self, vpc_id):
        print('test')
        response = self.ec2_service.describe_nat_gateways(
            Filters=[{
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }]
        )
        result = []
        print(response)

        if response['NatGateways'] !=[] or response['NatGateways'] != None :
            # get nat_id


            for nat_res in response['NatGateways']:
                nat_id = []
                nat_id.append(nat_res['NatGatewayId'])
                for i in nat_id:
                    result.append(self.describe_nat2(i, vpc_id))

        else:
            nat_id, nat_eip, nat_privte, vpc_id, sub_id = 'Not found', 'Not found', 'Not found', 'Not found', 'Not found'
            result.append((nat_id, nat_eip, nat_privte, vpc_id, sub_id))
        print(result)
        return result


    def describe_nat2(self, nat_id, vpc_id):
        response = self.ec2_service.describe_nat_gateways(
            Filters=[{
                'Name': 'nat-gateway-id',
                'Values': [nat_id]
            }]
        )


        nat_instance = response['NatGateways'][0]

        nat_id = nat_instance['NatGatewayId']
        sub_id = nat_instance['SubnetId']

        ips = nat_instance['NatGatewayAddresses'][0]
        nat_eip = ips['PublicIp']
        nat_privte = ips['PrivateIp']

        result = (nat_id, nat_eip, nat_privte, vpc_id, sub_id)

        return result