# Goal of this project

The goal of this script is to create many things quickly.

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

## Create a VPC

This script allow you create a vpc with a bastion for connect it from public network.

Bastion machine will be usefull for connect to other machine to your vpc.

## Todo 

 * Create argument for create custom vpc.
 * Improve common.py thank to dict.
