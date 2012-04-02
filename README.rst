Some helpers to make running Fabric tasks on EC2 instances a little easier.

Usage::

    from fabric.api import run, env
    from fabric_ec2 import get_instances_for_tags
    
    # Define a roledefs mapping to build a mapping of roles:hosts, based on the host's
    # EC2 tags
    env.roledefs = {
        # Search in a single, specified region...
        'webserver': get_instances_for_tags({'role': 'webserver'}, ['eu-west-1', ]),
        # ... or search all regions
        'dbserver': get_instances_for_tags({'role': 'dbserver'}),
    }

    @roles('webserver')
    def host_type():
        run('hostname')

Notes:

 * Make sure to set up AWS credentials, as described in the boto docs
 * Checking in all regions can be slow, restrict the server to a smaller number
   of regions if possible. Multiple roledefs can help here, e.g. create roledefs
   for "EU web servers", "US-1 web servers" and so on.


TODO:
    
 * setup.py
