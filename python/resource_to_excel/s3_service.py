class s3s:
    def __init__(self, s3_service):
        self.s3_service = s3_service


    def describe_s3s(self):
        #버킷 리스트 불러오기 (버킷 명 밖에 없음)
        s3_name_list = self.s3_service.list_buckets()

        print('--------------S3 버킷 네임 정보 ------------')
        print(s3_name_list)


        result = []
        region = 'ap-northeast-2'

        for s3_name_info in s3_name_list['Buckets']:
            bucket_name = s3_name_info['Name']
            life_name = ''
            life_class = ''
            life_move_date = ''
            life_delete_date = ''

            try:
                s3_ac_info = self.s3_service.get_bucket_policy(Bucket=s3_name_info['Name'])
            except:
                s3_ac_info = ''

            try:
                s3_life_info = self.s3_service.get_bucket_lifecycle(Bucket=s3_name_info['Name'])['Rules'][0]
                life_name = s3_life_info['ID']
                life_class = s3_life_info['Transition']['StorageClass']
                life_move_date = str(s3_life_info['Transition']['Days']) + '일 후'
                life_delete_date = str(s3_life_info['Expiration']['Days']) + '일 후'
            except:
                s3_life_info = ''

            result.append((bucket_name, region, life_name, life_class, life_move_date, life_delete_date))

        return result