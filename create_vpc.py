#!/usr/bin/env python
# encoding: utf-8

import common

AK, SK, AMI, KP, REGION = common.config()
cli, ec2 = common.boto_connector('ec2')

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
            bastion = subnet.create_instances(ImageId=AMI, InstanceType='t1.micro', KeyName=KP, MinCount=1, MaxCount=1)
            bastion_tags = {'Key':'Name','Value':'bastion'}
            bastion[0].create_tags(Tags=[bastion_tags])
        else:
            subnet_tags = {'Key':'Name','Value':'private'}
            subnet.create_tags(Tags=[subnet_tags])
    gateway = ec2.create_internet_gateway()
    gateway.attach_to_vpc(VpcId=vpc.id)
    bastion_ip = cli.allocate_address(Domain='vpc')
    cli.associate_address(InstanceId=bastion[0].id, AllocationId=bastion_ip['AllocationId'])

if __name__ == "__main__":
    create_vpc()
