class alb:
    def __init__(self, vpc_id, elb2):
        self.elb2 = elb2
        self.vpc_id = vpc_id

    def describe_not_classic_listeners(self, elb_arn):
        response = self.elb2.describe_listeners(LoadBalancerArn=elb_arn)

        return response['Listeners']

    def describe_not_classic_elb(self):
        response = self.elb2.describe_load_balancers()
        # target group 를위한 response
        target_response = self.elb2.describe_target_groups()

        elb_name = ''
        elb_arn = ''
        dns_name = ''
        port = ''
        target = ''
        az = ''
        host_count = ''
        health_check = ''
        result = []

        for balancer in response['LoadBalancers']:
            if balancer['VpcId'] == self.vpc_id:
                elb_name = balancer['LoadBalancerName']
                elb_arn = balancer['LoadBalancerArn']
                dns_name = balancer['DNSName']
                elb_type = balancer['Type']
                ip_type = balancer['IpAddressType']
                sg_name = ''
                az_name = ''
                target_arn_name = ''
                host_count = ''

                for az in balancer['AvailabilityZones']:
                    az_name += az['ZoneName'] + ', '

                try:
                    for sg in balancer['SecurityGroups']:
                        sg_name += sg + ', '
                except KeyError:
                    sg_name = '-'

                elb_listener = self.describe_not_classic_listeners(elb_arn)

                if elb_listener != []:
                    for i in elb_listener:
                        ports = i['Port']

                        # [190514]민걸 - TargetGroupArn 값이 없어서 애러가 남
                        try:
                            target = i['DefaultActions'][0]['TargetGroupArn'].split('/')
                            target_num = 0
                            for target_arn in target:
                                target_num += 1
                                if target_num == 2:
                                    target_arn_name += target_arn + ', '
                        except KeyError:
                            target = ' TargetGroupArn-none '
                        port += '{0} forwarding to {1}, '.format(ports, target)
                    host_count += '{} has been found as targets'.format(len(elb_listener))
                else:
                    port = 'None'
                    target = 'None'
                    host_count = 'None'
                health_check = 'No exists'

                result.append((elb_name, dns_name, elb_type, az_name, host_count))



        return result