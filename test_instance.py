#!/usr/bin/env python
# encoding: utf-8

import common
import create_instance
import sys

AK, SK, AMI, KP, REGION = common.config()
cli, ec2 = common.boto_connector('ec2')

if __name__ == "__main__":
    ans = "y"
    while ans == "y":
	if len(sys.argv) == 1:
	    name = ""
	else:
	    name = sys.argv[1]
	instanceId = create_instance.create_instance(vmName=name)
	print("Instance {} is created".format(instanceId))
	ans = raw_input("Do you want destroy and rebuild ? (y/n)")
	ids = list()
	ids.append(instanceId)
	ec2.instances.filter(InstanceIds=ids).terminate()
	print("Instance {} is removed".format(ids))
	ids.remove(instanceId)
