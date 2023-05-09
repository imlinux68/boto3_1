import boto3
from time import sleep


# Create an EC2 client
ec2_client = boto3.client('ec2')

# Create an EC2 instance
instance = ec2_client.run_instances(
    ImageId='ami-02d5619017b3e5162',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='newkey',
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
