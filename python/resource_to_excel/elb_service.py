class elb:
    def __init__(self, elb):
        self.elb = elb


    def describe_classic_listeners(self, elb_name):
        response = self.elb.describe_instance_health(LoadBalancerName=elb_name)

        return response['InstanceStates']

    def descrbie_classic_elb(self):
        response = self.elb.describe_load_balancers()

        elb_name = ''
        dns_name = ''
        port = ''
        az = ''
        instance_check = '_'
        host_count = ''
        health_check = ''
        result = []

        for elb in response['LoadBalancerDescriptions']:
            elb_name = elb['LoadBalancerName']
            dns_name = elb['DNSName']
            az = ''
            host_count = ''

            for i in elb['ListenerDescriptions']:
                port = '{0} forwarding to {1}'.format(i['Listener']['LoadBalancerPort'], i['Listener']['InstancePort'])

            for i in elb['AvailabilityZones']:
                az += i + ', '

            instance_check = self.describe_classic_listeners(elb_name)
            for i in instance_check:
                if i !=[]:
                    insid = i['InstanceId']
                    state = i['State']
                    host_count += '{0} is in {1}, '.format(insid, state)
                else:
                    host_count = 'No instances'

            health_check = elb['HealthCheck']

            result.append((elb_name, dns_name, port, az, host_count, health_check))

        return result