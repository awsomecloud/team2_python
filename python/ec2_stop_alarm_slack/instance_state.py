import boto3
import time

#from termcolor import colored

ec2 = boto3.resource('ec2')
def print_info(event):
    
    #time.sleep(60)
    
    instance_state = ""
    #종료 function = stopped 시작 function = running
    function_type = event
    function_name = ""
    if function_type == "stopped" :
        function_name = "인스턴스 자동종료"
    else :
        function_name = "인스턴스 자동시작"
    
    #비정상 체크
    abnormal_num = 0
    
    mail_text = ""
    #auto 목록만 불러오기
    filters = [{
            'Name': 'tag:auto',
            'Values': ['yes']
        }
    ]
    #for i in ec2.instances.all():
    for i in ec2.instances.filter(Filters=filters):
        if i.state['Name'] == function_type:
            instance_state = "성공"
        else :
            instance_state = "실패"
            abnormal_num += 1
        
        mail_text += "[{0}] Id: {1}\tState: {2}\tLaunched: {3} \n".format(
            instance_state,
            i.id,
            i.state['Name'],
            i.launch_time
            #i.root_device_name
        )
        
        mail_text += "\tArch: {0}\tHypervisor: {1} \n".format(
            i.architecture,
            i.hypervisor
        )
        
        mail_text += "\tPriv. IP: {0}\tPub. IP: {1} \n".format(
            i.private_ip_address,
            i.public_ip_address
        )
        
        mail_text += "\tPriv. DNS: {0}\tPub. DNS: {1} \n".format(
            i.private_dns_name,
            i.public_dns_name
        )
        
        mail_text += "\tSubnet: {0}\tSubnet Id: {1} \n".format(
            i.subnet,
            i.subnet_id
        )
        
        mail_text += "\tKernel: {0}\tInstance Type: {1} \n".format(
            i.kernel_id,
            i.instance_type
        )
        
        mail_text += "\tRAM Disk Id: {0}\tAMI Id: {1}\tPlatform: {2}\t EBS Optimized: {3} \n".format(
            i.ramdisk_id,
            i.image_id,
            i.platform,
            i.ebs_optimized
        )
    
        # print("\tBlock Device Mappings:")
        # for idx, dev in enumerate(i.block_device_mappings, start=1):
        #     print("\t- [{0}] Device Name: {1}\tVol Id: {2}\tStatus: {3}\tDeleteOnTermination: {4}\tAttachTime: {5}".format(
        #         idx,
        #         dev['DeviceName'],
        #         dev['Ebs']['VolumeId'],
        #         dev['Ebs']['Status'],
        #         dev['Ebs']['DeleteOnTermination'],
        #         dev['Ebs']['AttachTime']
        #     ))
        
        mail_text += "\tTags: \n"
        for idx, tag in enumerate(i.tags, start=1):
            mail_text += "\t- [{0}] {1} : {2} \n".format(
                idx,
                tag['Key'],
                tag['Value']
            )
        
    
        # print("\tProduct codes:")
        # for idx, details in enumerate(i.product_codes, start=1):
        #     print("\t- [{0}] Id: {1}\tType: {2}".format(
        #         idx,
        #         details['ProductCodeId'],
        #         details['ProductCodeType']
        #     ))
    
        #print("Console Output:")
        # print(i.console_output()['Output'])
        
        mail_text += "--------------------\n"
        
    if(abnormal_num > 0) :
        mail_text = "\t- {0} 실패하였습니다. \n 실패 인스턴스 수 : {1}\n {2}".format(
            function_name,
            str(abnormal_num),
            mail_text
        )
    else :
        mail_text = "\t- {0} 성공하였습니다. \n {1}".format(
            function_name,
            mail_text
        )
    print(mail_text)
    
    return mail_text
