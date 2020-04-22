class ws:
    def __init__(self, workspace, ec2, vpc_id):
        self.workspace = workspace
        self.ec2 = ec2
        self.vpc_id = vpc_id

    def describe_workspace_info(self):
        directories_info = self.workspace.describe_workspace_directories()

        directories_id = []
        for dir_info in directories_info['Directories']:
            subnet_id = dir_info['SubnetIds'][0]

            subnet_info = self.ec2.describe_subnets(
                SubnetIds=[
                    subnet_id
                ]
            )
            vpc_id = subnet_info['Subnets'][0]['VpcId']
            if self.vpc_id == vpc_id:
                directories_id.append(dir_info['DirectoryId'])

        result = []

        for dir_id in directories_id :
            response = self.workspace.describe_workspaces(
                DirectoryId=dir_id
            )

            for ws_info in response['Workspaces']:
                ws_id = ws_info['WorkspaceId']
                ws_username = ws_info['UserName']
                ws_status = ws_info['State']

                ws_runmode = ws_info['WorkspaceProperties']['RunningMode']
                ws_rootsize = str(ws_info['WorkspaceProperties']['RootVolumeSizeGib']) + ' GiB'
                ws_usersize = str(ws_info['WorkspaceProperties']['UserVolumeSizeGib']) + ' GiB'
                ws_cputype = ws_info['WorkspaceProperties']['ComputeTypeName']

                result.append((ws_id, ws_username, ws_status, ws_runmode, ws_rootsize, ws_usersize,
                               ws_cputype))

        return result