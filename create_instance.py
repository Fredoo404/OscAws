#!/usr/bin/env python
# encoding: utf-8

import common
import argparse

AK, SK, AMI, KP, REGION = common.config()
cli, ec2 = common.boto_connector('ec2')

def create_instance(config=None, insType='t1.micro', omi=AMI, keyPair=KP,ebsSize=None, vmName=""):
    """
        Function which will create an instance with parameters configured.
    """
    if config is not None:
        with open(config, 'r') as files:
            userdata = files.read()
    else:
        userdata = ''
    instance_tags = {'Key':'Name','Value':vmName}
    instance = ec2.create_instances(ImageId=omi, InstanceType=insType, KeyName=keyPair, UserData=userdata, MinCount=1, MaxCount=1)[0]
    instance.create_tags(Tags=[instance_tags])
    if ebsSize != None:
        vol = ec2.create_volume(Size=ebsSize, AvailabilityZone=EC2region + "a")
	while instance.state['Name'] != 'running':
		instance.reload()
        instance.attach_volume(VolumeId=vol.id, Device="/dev/xvdb")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Instance script')
    parser.add_argument('-n', dest='vmname', help='VM name (Default: foobar)', default='foobar')
    parser.add_argument('-t', dest='instancetype', help='Instance type (Default: m4.large)', default='m4.large')
    parser.add_argument('-o', dest='ami', help='AMI/OMI (Default: Define in .config file)', default=AMI)
    parser.add_argument('-k', dest='keypair', help='Key Pair (Default: Define in .config file)', default=KP)
    parser.add_argument('-e', dest='ebs', help='Ebs size', default=None)
    parser.add_argument('-u', dest='userdata', help='Cloud-init config', default=None)

    argVmname = parser.parse_args().vmname
    argInstancetype = parser.parse_args().instancetype
    argAmi = parser.parse_args().ami
    argKeypair = parser.parse_args().keypair
    argEbs = parser.parse_args().ebs
    argUserdata = parser.parse_args().userdata
    create_instance(vmName=argVmname, config=argUserdata, insType=argInstancetype, omi=argAmi, keyPair=argKeypair, ebsSize=argEbs)
