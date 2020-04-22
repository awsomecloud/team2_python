class tg:
    def __init__(self, vpc_id, elb2):
        self.elb2 = elb2
        self.vpc_id = vpc_id


    def describe_alb_name(self, alb_arn):
        response = self.elb2.describe_load_balancers(LoadBalancerArns=[alb_arn])

        return response['LoadBalancers']

    def describe_target_groups(self):
        response = self.elb2.describe_target_groups()

        result = []

        for balancer in response['TargetGroups']:
            if balancer['VpcId'] == self.vpc_id:

                protocol = balancer['Protocol']
                tg_name = balancer['TargetGroupName']
                port = balancer['Port']

                h_protocol = balancer['HealthCheckProtocol']
                h_port = balancer['HealthCheckPort']
                h_Intervalseconds = balancer['HealthCheckIntervalSeconds']
                h_timeoutseconds = balancer['HealthCheckTimeoutSeconds']
                h_ThresholdCount = balancer['HealthyThresholdCount']
                uh_ThresholdCount = balancer['UnhealthyThresholdCount']
                try:
                    h_path = balancer['HealthCheckPath']
                except KeyError:
                    h_path = '-'

                alb_name = ''


                alb_arn = balancer['LoadBalancerArns']
                for alb_arn_info in alb_arn:
                    alb_response = self.describe_alb_name(alb_arn_info)

                    if alb_response != []:
                        for i in alb_response:
                            alb_name += i['LoadBalancerName']


                result.append((tg_name, port, h_protocol, h_Intervalseconds, h_timeoutseconds, h_ThresholdCount, uh_ThresholdCount, h_path, alb_name))
        return result