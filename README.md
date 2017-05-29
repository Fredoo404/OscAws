# Goal of this project

The goal of this set of script is to create many things quickly.

This script work on Outscale and AWS cloud.

## How use this script ?

For use this python script, you need ton create a .config file with content below :

 ```bash
 AK=XXXXXXXXXXXXXXXXXXX
 SK=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
 DEFAULT_AMI=ami-xxxxxxxx
 KEYPAIR=your_keypair
 REGION=us-east-2 
 ```
Then launch this script of your choice like below :

 ```python
 python create_vpc.py
 ```
## Create an instance (create_instance.py)

This script without parameter allow you create a basic instance.

You can put parameter below if your want a custom instance :

 ```bash
usage: create_instance.py [-h] [-n VMNAME] [-t INSTANCETYPE] [-o AMI]
                          [-k KEYPAIR] [-e EBS] [-u USERDATA]

Create Instance script

optional arguments:
  -h, --help       show this help message and exit
  -n VMNAME        VM name (Default: foobar)
  -t INSTANCETYPE  Instance type (Default: m4.large)
  -o AMI           AMI/OMI (Default: Define in .config file)
  -k KEYPAIR       Key Pair (Default: Define in .config file)
  -e EBS           Ebs size
  -u USERDATA      Cloud-init config
 ```

## Create a VPC

This script allow you create a vpc with a bastion for connect it from public network.

Bastion machine will be usefull for connect to other machine to your vpc.

## Todo 

 * Create argument for create custom vpc.
 * Improve common.py thank to dict.
 * Make choice during creation of ebs (in create_instance.py)
