import concurrent.futures

class iam:

    def __init__(self, iam_service, access_yn):
        self.iam_service = iam_service
        self.access_yn = access_yn



    def describe_iam_user_info(self):
        response = self.iam_service.list_users()

        result = []

        how_use = '구축'
        passwd = '-'
        etc = ''

        for iam_info in response['Users']:
            arn = iam_info['Arn']
            arn_split = arn.split(':')

            #get account Number
            account_num = arn_split[4]

            #get Console Url
            console_url = 'https://' + account_num + '.signin.aws.amazon.com/console'
            user_name = iam_info['UserName']

            #get group Name
            iam_group = self.iam_service.list_groups_for_user(
                UserName=user_name
            )
            group_name = ''
            for group_info in iam_group['Groups']:
                group_name += group_info['GroupName'] + ', '

            etc = ''
            if self.access_yn == 'y':
                # get 엑세스키
                access_list = self.iam_service.list_access_keys(
                    UserName=user_name
                )
                etc = ''
                for access_info in access_list['AccessKeyMetadata']:
                    etc += access_info['AccessKeyId'] + ' | '

            if self.access_yn == 'y':
                result.append((user_name, etc, passwd, group_name, ''))
            else:
                result.append((account_num, how_use, console_url, user_name, passwd, group_name, etc))

        return result


    #iam role 내 적용 된 Policies 목록
    def get_role_policies_list(self, role_name):
        policies_list = self.iam_service.list_attached_role_policies(
            RoleName=role_name
        ).get('AttachedPolicies', [])
        policies_result = ''
        for policies_info in policies_list:
            if policies_info is policies_list[-1]:
                policies_result += policies_info['PolicyName']
            else:
                policies_result += policies_info['PolicyName'] + '\n'

        return (role_name, policies_result, '')


    def describe_iam_role_info(self):
        role_result = []
        role_list = self.iam_service.list_roles().get('Roles', [])
        role_name_list = []

        for role_info in role_list:
            if 'AWSServiceRole' in role_info['RoleName']:
                #aws에서 생성한 role 일경우
                print('기존 role')
            else:
                role_name_list.append(role_info['RoleName'])

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            #secs = [5, 4, 3, 2, 1]
            results = [executor.submit(self.get_role_policies_list, role_name) for role_name in role_name_list]
            for f in concurrent.futures.as_completed(results):
                #print(f.result())
                #print("ec2 threading")
                role_result.append(f.result())
        print('IAM USER GROUP 정보')
        print(role_result)
        return role_result

        # iam group 내 적용 된 Policies 목록
    def get_group_policies_list(self, group_name):
        print('IAM group_name 정보')
        print(group_name)
        policies_list = self.iam_service.list_attached_group_policies(
            GroupName=group_name
        ).get('AttachedPolicies', [])
        policies_result = ''
        for policies_info in policies_list:
            if policies_info is policies_list[-1]:
                policies_result += policies_info['PolicyName']
            else:
                policies_result += policies_info['PolicyName'] + '\n'

        return (group_name, policies_result, '')

    #iam 그룹 가져오기
    def describe_iam_group_info(self):
        group_result = []
        group_list = self.iam_service.list_groups().get('Groups', [])

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            #secs = [5, 4, 3, 2, 1]
            results = [executor.submit(self.get_group_policies_list, group_name['GroupName']) for group_name in group_list]
            for f in concurrent.futures.as_completed(results):
                #print(f.result())
                #print("ec2 threading")
                group_result.append(f.result())
        print('IAM USER GROUP 정보')
        print(group_result)
        return group_result