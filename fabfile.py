from fabric.api import run, env, roles
from fabric_ec2 import get_instances_for_tags

# Define a roledefs mapping to build a mapping of roles:hosts, based on the host's
# EC2 tags
env.roledefs = {
    # Search in a single, specified region...
    'webserver': get_instances_for_tags({'Name': 'puppet.goteam.be'}, ['eu-west-1', ]),
    # ... or search all regions
    #'dbserver': get_instances_for_tags({'role': 'dbserver'}),
}

@roles('webserver')
def host_type():
    run('hostname')

