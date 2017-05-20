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

def create_vpc():
    """
        Function which will create a vpc with:
          - 2 subnets (192.168.0.0/25 and 192.168.0.128/25)
          - create internet gateway and attach it to vpc.
          - create an instance on public subnet
          - associate public ip on this instance.

           # Create standard vpc
            create_vpc()

    """
    cidr_vpc = '192.168.0.0/24'
    cidr_subnet = ['192.168.0.0/25','192.168.0.128/25']
    vpc_tags = {'Key':'Name','Value':'foobar'}
    vpc = ec2.create_vpc(CidrBlock=cidr_vpc)
    vpc.create_tags(Tags=[vpc_tags])
    for i in cidr_subnet:
        subnet = vpc.create_subnet(CidrBlock=i)
        if i == cidr_subnet[0]:
            subnet_tags = {'Key':'Name','Value':'public'}
            subnet.create_tags(Tags=[subnet_tags])
            bastion = subnet.create_instances(ImageId=default_omi, InstanceType='t1.micro', KeyName=key_pair, MinCount=1, MaxCount=1)
            bastion_tags = {'Key':'Name','Value':'bastion'}
            bastion[0].create_tags(Tags=[bastion_tags])
        else:
            subnet_tags = {'Key':'Name','Value':'private'}
            subnet.create_tags(Tags=[subnet_tags])
    gateway = ec2.create_internet_gateway()
    gateway.attach_to_vpc(VpcId=vpc.id)
    bastion_ip = cli.allocate_address(Domain='vpc')
    cli.associate_address(InstanceId=bastion[0].id, AllocationId=bastion_ip['AllocationId'])

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
