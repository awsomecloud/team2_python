import concurrent.futures

class endpoint:

    def __init__(self, endpoint_service, vpc_id):
        self.endpoint_service = endpoint_service
        self.vpc_id = vpc_id

    def describe_endpoint_info(self):
        result = []
        vpc_id = self.vpc_id
        endpoint_list = self.endpoint_service.describe_vpc_endpoints(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ]
        )

        for endpoint_info in endpoint_list['VpcEndpoints']:

            endpoint_name = ''
            endpoint_type = endpoint_info['VpcEndpointType']
            endpoint_id = endpoint_info['VpcEndpointId']
            vpc_id_info = endpoint_info['VpcId']
            serivce_name = endpoint_info['ServiceName']
            u_description = ''

            if endpoint_info.get('Tags') != None:
                for endpoint_tag_info in endpoint_info['Tags']:
                    if endpoint_tag_info['Key'] == 'Name':
                        endpoint_name = endpoint_tag_info['Value']

            result.append((endpoint_name, endpoint_id, vpc_id_info, endpoint_type, serivce_name, u_description))

        return result