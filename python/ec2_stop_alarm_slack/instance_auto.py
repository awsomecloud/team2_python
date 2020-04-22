import boto3
import logging
region = 'ap-northeast-2'
ins_list = []
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def instances_stop():
    ec2 = boto3.resource('ec2')
    filters = [{
            'Name': 'tag:auto',
            'Values': ['yes']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
    instances = ec2.instances.filter(Filters=filters)
    #필터에 맞는 인스턴스 id 리스트화
    StartInstances = [instance.id for instance in instances]
    #인스턴스 종료
    ec2.instances.filter(InstanceIds=StartInstances).stop()

def instances_start():
    ec2 = boto3.resource('ec2')
    filters = [{
            'Name': 'tag:auto',
            'Values': ['yes']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)
    StoppedInstances = [instance.id for instance in instances]
    #인스턴스 시작
    ec2.instances.filter(InstanceIds=StoppedInstances).start()