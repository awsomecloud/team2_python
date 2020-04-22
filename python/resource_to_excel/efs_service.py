import math
class ef:
    def __init__(self, efs, ec2, vpc_id, region_id):
        self.efs = efs
        self.ec2 = ec2
        self.vpc_id = vpc_id
        self.region_id = region_id

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GiB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def describe_efs_info(self):

        file_system_info = self.efs.describe_file_systems()

        fs_id_list_first = []

        result = []
        print('------------------------efs----------------------------')
        print(file_system_info)

        for fs_info in file_system_info['FileSystems']:

            fs_id = ''
            size = ''
            p_mode_nm = ''
            subnet_ip = ''
            dns_nm = ''
            sg_nm = ''


            mount_target_info = self.efs.describe_mount_targets(
                FileSystemId=fs_info['FileSystemId']
            )

            subnet_info = self.ec2.describe_subnets(
                        SubnetIds=[
                            mount_target_info['MountTargets'][0]['SubnetId']
                        ]
                    )
            vpc_id = subnet_info['Subnets'][0]['VpcId']
            if self.vpc_id == vpc_id:
                fs_id = fs_info['FileSystemId']
                size = self.convert_size(int(fs_info['SizeInBytes']['Value']))
                p_mode_nm = fs_info['PerformanceMode']
                dns_nm = fs_id + '.' + 'efs.' + self.region_id + '.amazonaws.com'

                for mt_info in mount_target_info['MountTargets']:
                    subnet_ip += 'subnetID : ' + mt_info['SubnetId'] + ' ,IP : ' + mt_info['IpAddress'] + ' | '
                    sg_list = self.efs.describe_mount_target_security_groups(MountTargetId=mt_info['MountTargetId'])
                    for sg_info in sg_list['SecurityGroups']:
                        sg_nm += sg_info + ', '
                tag_name = ' - '
                for tag_info in fs_info['Tags']:
                    if tag_info['Key'] == 'Name':
                        tag_name = tag_info['Value']

                result.append((tag_name, fs_id, size, p_mode_nm, subnet_ip, dns_nm, sg_nm))

        return result