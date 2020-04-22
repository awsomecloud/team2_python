class cloudfront:

    def __init__(self, cloudfront_service):
        self.cf = cloudfront_service

    def describe_cfs(self):
        response = self.cf.list_distributions()
        result = []

        etc = ''
        try:
            for cf_info in response['DistributionList']['Items']:
                cf_origin = ''
                cf_cname = ''
                ids = cf_info['Id']
                cf_domain = cf_info['DomainName']
                for origin_info in cf_info['Origins']['Items']:
                    cf_origin += origin_info['DomainName']

                try:
                    for cname_info in cf_info['Aliases']['Items']:
                        cf_cname += cname_info + ', '
                except KeyError:
                    cf_cname = '-'

                result.append((ids, cf_domain, cf_origin, cf_cname, etc))
        except KeyError:
            result.append(('-', '-', '-', '-', '-'))

        return result


