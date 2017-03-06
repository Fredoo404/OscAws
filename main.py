#!/usr/bin/env python
# encoding: utf-8

import boto3

default_omi = 'ami-d4f2f835'

with open('.config','r') as config:
  AK, SK = config.read().rstrip().split('\n')

EC2endpoint = "https://fcu.eu-west-2.outscale.com"
EC2region = "eu-west-2"

ec2 = boto3.resource(service_name='ec2', region_name=EC2region, endpoint_url=EC2endpoint, aws_access_key_id=AK, aws_secret_access_key=SK)

def create_vpc():
  cidr_vpc = '192.168.0.0/24'
  cidr_subnet = ['192.168.0.0/25','192.168.0.128/25']
  vpc = ec2.create_vpc(CidrBlock=cidr_vpc)
  for i in cidr_subnet:
    subnet = vpc.create_subnet(CidrBlock=i)
  gateway = ec2.create_internet_gateway()
  # TODO :
  # 1/ Link to vpc in subnet public.
  # 2/ Add Name tags with name associate.
  bastion = ec2.create_instances(ImageId=default_omi, InstanceType='t1.micro', MinCount=1, MaxCount=1)

create_vpc()