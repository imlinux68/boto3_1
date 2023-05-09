#!/bin/python

#import boto3
#from time import sleep


#def describe_instance():
#    client = boto3.client('ec2')
#    response = client.describe_instances()
#    for r in response['Reservations']:
#        for i in r['Instances']:
#            print("ID: " + i['InstanceId'] + "\nIP Address: " + i['PublicIpAddress'] +  "\n----------------------------------------\n"  )
           
#describe_instance()

import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError

def describe_instances():
    try:
        client = boto3.client('ec2')
        response = client.describe_instances()
        for r in response['Reservations']:
            for i in r['Instances']:
                instance_id = i['InstanceId']
                public_ip = i.get('PublicIpAddress', 'N/A')
                print("ID: {}\nIP Address: {}\n----------------------------------------".format(instance_id, public_ip))
    except NoCredentialsError:
        print("Failed to get AWS credentials. configure your credentials again with (aws configure).")
    except BotoCoreError as e:
        print("Error while describing instances: {}".format(e))

describe_instances()
