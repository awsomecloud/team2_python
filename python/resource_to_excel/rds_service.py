import re
class rds:

    def __init__(self, vpc_id, rds_service):
        self.rds = rds_service
        self.vpc_id = vpc_id

    def get_db_arn(self):
        response = self.rds.describe_db_instances()

        print('--------------DB instance 정보 ------------')
        print(response)
        print('--------------DB instance 정보 끝 ------------')

        result = []
        arn = []
        for i in response['DBInstances']:
            #[민걸] VPC 나누어서 나오기 190524
            if i['DBSubnetGroup']['VpcId'] == self.vpc_id:
                arn.append(i['DBInstanceArn'])

        for j in arn:
            result.append(self.describe_rds(j))

        return result

    def describe_rds(self, db_arn):
        response = self.rds.describe_db_instances(
            Filters=[{
                'Name': 'db-instance-id',
                'Values': [db_arn]
            }]
        )

        db_instance = response['DBInstances'][0]

        arn = db_instance['DBInstanceIdentifier']
        #[민걸]DBInstanceIdentifier - > DBName으로 수정하였음 - 19.04.10 -
        #[민걸]MS DB의 경우 나 DB Name가 없는경우 Key 애러가 남  - > try except 문으로 오류시 '-' 입력 - 19.04.11 -
        try:
            db_name = db_instance['DBName']
        except KeyError:
            db_name = '-'

        #보안 그룹 추가(2019.04.25 - 민거리)
        db_sg = []
        # [민걸] 시큐리티 그룹 DB -> vpc 로 수정 190524
        for i in db_instance['VpcSecurityGroups']:
            db_sg.append(i['VpcSecurityGroupId'])

        # 서브넷 그룹 추가(2019.04.25 - 민거리)
        db_subnet_gp = db_instance['DBSubnetGroup']['DBSubnetGroupName']
        # 파라미터 그룹 추가(2019.04.25 - 민거리)
        db_para_gp_string = ''
        #for j,i in enumerate(db_instance['DBParameterGroups']):
        for i in db_instance['DBParameterGroups']:
            db_para_gp_string += i['DBParameterGroupName'] + ' | '

        #----------------------------------------

        db_engine = db_instance['Engine']
        db_type = db_instance['DBInstanceClass']
        db_storage = db_instance['AllocatedStorage']
        db_id = db_instance['MasterUsername']
        db_pw = 'Manual needed'
        db_characterset = 'Manual needed'
        db_mulaz = db_instance['MultiAZ']
        db_public = db_instance['PubliclyAccessible']
        db_endpoint = db_instance['Endpoint']['Address']

        result = (arn, db_name, db_engine, db_type, db_storage, db_id, db_pw, db_characterset, db_mulaz, db_public, db_endpoint, db_sg, db_subnet_gp, db_para_gp_string)

        return result
