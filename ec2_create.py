#!/bin/python

import boto3

ec2 = boto3.resource('ec2')

#create new ec2

instances = ec2.create_instances(
    ImageId='ami-02d5619017b3e5162',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='newkey',
    UserData='''#!/bin/bash
                # Install Docker
                yum update -y && yum install git -y
                amazon-linux-extras install docker -y
                service docker start
                usermod -aG docker ec2-user

                # Install Docker Compose
                yum install python3-pip -y
                pip3 install docker-compose
                '''
 )

