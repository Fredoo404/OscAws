#!/usr/bin/env python
# encoding: utf-8

def config():
    """
    Manage configuration files.
    """
    with open('.config','r') as config:
      AK, SK, AMI, KP = config.read().rstrip().split('\n')
    AK=AK.split('=')[1]
    SK=SK.split('=')[1]
    AMI=AMI.split('=')[1]
    KP=KP.split('=')[1]

    return AK, SK, AMI, KP

if __name__ == "__main__":
    print(config())
