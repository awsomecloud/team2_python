import xml.etree.ElementTree as ES


class vpn:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    # vpc_id is list type
    def describe_vpn_gates(self, vpc_id):
        response = self.ec2_service.describe_vpn_gateways(
            Filters=[{
                'Name': 'attachment.vpc-id',
                'Values': [vpc_id]
            }]
        )


        result = []
        if response['VpnGateways'] != []:

            response_detail = self.ec2_service.describe_vpn_connections(
                Filters=[{
                    'Name': 'vpn-gateway-id',
                    'Values': [response['VpnGateways'][0]['VpnGatewayId']]
                }]
            )

            # for key, value in response_detail.items():
            # print('vpn01 : ' + key, ":", value)

            # get amazon side asn
            amazonesideasn = response['VpnGateways'][0]['AmazonSideAsn']

            for vpn_info in response_detail['VpnConnections']:

                # save value
                vpn_name = ''
                tunnels = []
                static_routes = []
                customerGatewayConfiguration_xml = []

                # get CustomerGatewayConfiguration xml
                item = ''
                test01 = 0
                print(vpn_info)

                # get name
                for tag in vpn_info['Tags']:
                    if tag['Key'] == 'Name':
                        vpn_name = tag['Value']

                # get tunnel ip
                try:
                    for tunnel in vpn_info['VgwTelemetry']:
                        tunnels.append(tunnel['OutsideIpAddress'])
                    tunnel1 = tunnels[0]
                    tunnel2 = tunnels[1]
                except KeyError:
                    tunnel1 = '-'
                    tunnel2 = '-'


                # get customer_gate_id
                customer_gate_id = vpn_info['CustomerGatewayId']

                #[190524]get customer_gate_ip 추가
                customer_detail = self.ec2_service.describe_customer_gateways(
                    CustomerGatewayIds=[customer_gate_id]
                )

                customer_ip = ''
                for customer_info in customer_detail['CustomerGateways']:
                    customer_ip += customer_info['IpAddress']

                # get vpn_connection_id
                vpn_connection_id = vpn_info['VpnConnectionId']

                # get static_routes
                for route in vpn_info['Routes']:
                    static_routes.append(route['DestinationCidrBlock'])

                etc = ''

                result.append((vpn_name, customer_gate_id, vpn_connection_id, customer_ip, amazonesideasn, tunnel1,
                               tunnel2, static_routes, etc))

        else:
            vpn_name, customer_gate_id, vpn_connection_id, customer_ip, amazonesideasn, tunnel1, tunnel2, static_routes, etc = 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found'
            result.append((vpn_name, customer_gate_id, vpn_connection_id, customer_ip, amazonesideasn, tunnel1, tunnel2,
                           static_routes, etc))

        return result