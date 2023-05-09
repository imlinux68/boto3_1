#!/bin/python

import boto3

instances = input("Enter the IDs of instances you want to destroy (with comma separation!!!): ")
ids = instances.split(",")

# Create EC2 resource object
ec2 = boto3.resource('ec2')

# Terminate instances with for loop
for instance_id in ids:
    ec2.instances.filter(InstanceIds=[instance_id]).terminate()

print("Instances terminated successfully!")
