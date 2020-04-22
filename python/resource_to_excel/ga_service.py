class ga:
    def __init__(self, ga):
        self.global_ac = ga

    def describe_ga_info(self):
        ga_value = self.global_ac.list_accelerators()

        result = []
        for ga_info in ga_value['Accelerators']:
            name = ga_info['Name']
            enabled = ga_info['Enabled']
            status = ga_info['Status']
            ipsets = ''
            createdtime = ga_info['CreatedTime']
            modifiedtime = ga_info['LastModifiedTime']

            for ip_info in ga_info['IpSets']:
                ipsets += str(ip_info['IpAddresses']) + ' | '



            result.append((name, ipsets, enabled, status, createdtime, modifiedtime))
        #directories_id = []
        #for ga_info in ga_value['Directories']:

        return result

    def describe_listeners(self):
        ga_value = self.global_ac.list_accelerators()
        print(ga_value)

        #for ga_info in ga_value:

        # directories_id = []
        # for ga_info in ga_value['Directories']:

        # result.append((name, staticip, enabled, status, created, edited))
        result = ''

        return result

    def describe_(self):
        ga_value = self.global_ac.list_accelerators()
        print(ga_value)

        #for ga_info in ga_value:

        # for ga_info in ga_value['Directories']:

        # result.append((name, staticip, enabled, status, created, edited))
        result = ''

        return result