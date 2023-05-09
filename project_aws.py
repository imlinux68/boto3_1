#!/bin/python
from time import sleep
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


def deploy_instance():
    ec2_client = boto3.client('ec2')

    with open('/home/user/.ssh/ec2-instances.pub', 'r') as f:
        pub_key = f.read()

    response = ec2_client.import_key_pair(
        KeyName='ec2-instances',
        PublicKeyMaterial=pub_key
    )

    print(response)


    # Create an EC2 instance
    instance = ec2_client.run_instances(
        ImageId='ami-02d5619017b3e5162',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='ec2-instances',
        UserData='''#!/bin/bash
    yum update -y
    yum install git -y
    # Install Docker
    amazon-linux-extras install docker -y

    # Start Docker service
    systemctl start docker
    systemctl enable docker

    # Install Docker Compose
    curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    export PATH="/usr/local/bin:$PATH"
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

    # Get Docker Compose file from GitHub repository
    git clone https://github.com/imlinux68/flask-movie.git
    export PATH="/usr/local/bin:$PATH"

    # Change to the /docker-compose directory
    cd ./flask-movie

    # Run Docker Compose
    docker-compose up -d
                    ''',
    )

    instance_id = instance['Instances'][0]['InstanceId']
    print(f'Instance ID: {instance_id}')

    # Create a security group
    ec2_resource = boto3.resource('ec2')
    security_group = ec2_resource.create_security_group(
        GroupName='my-security-group',
        Description='My security group'
    )

    security_group_id = security_group.id
    print(f'Security Group ID: {security_group_id}')

    # Allow inbound traffic for ports 8081, 5000, and 27017
    security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8081, 'ToPort': 8081, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 5000, 'ToPort': 5000, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 27017, 'ToPort': 27017, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        ],
    )

    # Attach the security group to the instance
    ec2_client.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[security_group_id]
    )

    print('Instance created and security group configured successfully!')


def destroy_instance():
    instances = input("Enter the IDs of instances you want to destroy (with comma separation!!!): ")
    ids = instances.split(",")

    # Create EC2 resource object
    ec2 = boto3.resource('ec2')

    # Terminate instances with for loop
    for instance_id in ids:
        ec2.instances.filter(InstanceIds=[instance_id]).terminate()

    print("Instances terminated successfully!")


def stop_instance():
    instances = input("Enter the IDs of instances you want to stop (comma-separated): ")
    ids = instances.split(",")

    # Create EC2 resource object
    ec2 = boto3.resource('ec2')

    # Stop instances with for loop
    for instance_id in ids:
        ec2.instances.filter(InstanceIds=[instance_id]).stop()

    print("Instances stoped successfully!")

def start_instance():
    instances = input("Enter the IDs of instances you want to start (comma-separated): ")
    ids = instances.split(",")

    # Create EC2 resource object
    ec2 = boto3.resource('ec2')

    # Starting instances with for loop
    for instance_id in ids:
        ec2.instances.filter(InstanceIds=[instance_id]).start()

    print("Instances started successfully!")

def menu ():
    while(True):
        choice=input("Menu:\n1. Describe ec2 instances\n2. Deploy ec2 instances\n3. Destroy ec2 instances\n4. Stop ec2 instances\n5. Start ec2 instances\n")
        if(choice=="1"):
            print("Now you will see your instances:....\n")
            sleep(3)
            describe_instances()
        elif(choice=="2"):
            print("Now we will deploy your instances:....\n")
            sleep(3)
            deploy_instance()
        elif(choice=="3"):
            print("Now we will destroy your instances:....\n")
            sleep(3)
            destroy_instance()
        elif(choice=="4"):
            print("Now we will stop your instances:....\n")
            sleep(3)
            stop_instance()
        elif(choice=="5"):
            print("Now we will start your instances:....\n")
            sleep(3)
            start_instance()
        else:
            print("Enter 1-5 ONLY!!!!\n")
            continue
        exit=input("Do you wanna to exit? yes/no\n")
        if(exit=="yes"):
            print("Bye....")
            break
            
            
######MAIN SCRIPT###########

menu()


