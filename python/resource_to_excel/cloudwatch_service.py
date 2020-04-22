class cw:
    def __init__(self, cw_service):
        self.cw_service = cw_service


    def describe_cw(self):
        #버킷 리스트 불러오기 (버킷 명 밖에 없음)
        cw_list = self.cw_service.list_rules()

        result = []
        for cw_info in cw_list['Rules']:
            if cw_info.get('ScheduleExpression') != None:
                role_name = ''
                description = ''
                cron = ''
                target = ''
                input_data = ''
                role_name = cw_info['Name']
                try:
                    description = cw_info['Description']
                except KeyError:
                    description = ' '
                cron = cw_info['ScheduleExpression']

                role_target_list = self.cw_service.list_targets_by_rule(Rule=role_name)['Targets']
                for role_target_info in role_target_list:
                    arn = role_target_info['Arn']
                    arn_info_list = arn.split(':')
                    service_name = arn_info_list[2]
                    function_name = arn_info_list[-1]
                    target += service_name + ' : ' + function_name
                    try:
                        input_data += role_target_info['Input']
                    except KeyError:
                        input_data += ' '


                result.append((role_name, description, cron, target, input_data))

        return result