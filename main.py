#!/usr/bin/env python
# encoding: utf-8

import boto3
import time

default_omi = 'ami-d4f2f835' # Centos 7 eu-west-2
#default_omi = 'ami-6058c4d0'  # Centos 7 us-west-1
key_pair = 'osc'

with open('.config','r') as config:
  AK, SK = config.read().rstrip().split('\n')

#EC2endpoint = "https://fcu.us-west-1.outscale.com"
EC2endpoint = "https://fcu.eu-west-2.outscale.com"
EC2region = "eu-west-2"
#EC2region = "us-west-1"

cli = boto3.client(service_name='ec2', region_name=EC2region, endpoint_url=EC2endpoint, aws_access_key_id=AK, aws_secret_access_key=SK)
ec2 = boto3.resource(service_name='ec2', region_name=EC2region, endpoint_url=EC2endpoint, aws_access_key_id=AK, aws_secret_access_key=SK)

def create_instance(config=None, InsType='t1.micro', Omi=default_omi, ebsSize=None):
    """
        Function which will create an instance with parameters configured.
            # Create default instance 
            create_instance()

            # Create an m4.large with an ebs of 20G.
            create_instance(InsType='m4.large', Omi='ami-878aeda0', ebsSize=20)

            # Create an instance with cloud-init configuration in user-data.
            create_instance(config='/Users/frederic/Dropbox/dev/OscAws/cloud-init/basic', InsType='m4.large', Omi='ami-878aeda0', ebsSize=20)
    """
    if config is not None:
        with open(config, 'r') as files:
            userdata = files.read()
    else:
        userdata = ''
    instance_tags = {'Key':'Name','Value':'foobar'}
    instance = ec2.create_instances(ImageId=Omi, InstanceType=InsType, KeyName=key_pair, UserData=userdata, MinCount=1, MaxCount=1)[0]
    instance.create_tags(Tags=[instance_tags])
    if ebsSize != None:
        vol = ec2.create_volume(Size=ebsSize, AvailabilityZone=EC2region + "a")
	while instance.state['Name'] != 'running':
		instance.reload()
        instance.attach_volume(VolumeId=vol.id, Device="/dev/xvdb")
