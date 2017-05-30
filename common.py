#!/usr/bin/env python
# encoding: utf-8

import boto3

def config():
    """
    Manage configuration files.
    """
    with open('.config','r') as config:
      AK, SK, AMI, KP, REGION = config.read().rstrip().split('\n')
    AK=AK.split('=')[1]
    SK=SK.split('=')[1]
    AMI=AMI.split('=')[1]
    KP=KP.split('=')[1]
    REGION=REGION.split('=')[1]

    return AK, SK, AMI, KP, REGION

def boto_connector(service='ec2'):
    """
    Boto connector
    """
    AK, SK, AMI, KP, REGION = config() 
    cli = boto3.client(service_name=service, region_name=REGION, aws_access_key_id=AK, aws_secret_access_key=SK)
    ser = boto3.resource(service_name=service, region_name=REGION, aws_access_key_id=AK, aws_secret_access_key=SK)

    return cli, ser


if __name__ == "__main__":
    print(config())
