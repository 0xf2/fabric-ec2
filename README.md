Some helpers to make running Fabric tasks on EC2 instances a little easier.

You can use [EC2 Tags](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-tags.html) to assign tags to your instances describing their roles. For example, your webserver instances could be tagged with 'role=web'.

This helper class lets you use these tags on conjunction with Fabric's role definitions, by dynamically querying the EC2 API to find the instances that have been assigned a particular role.

Usage
=====
```python
    from fabric.api import run, sudo, env
    from fabric_ec2 import EC2TagManager

    def configure_roles(environment):
        """ Set up the Fabric env.roledefs, using the correct roles for the given environment
        """
        tags = EC2TagManager(AWS_KEY, AWS_SECRET,
            regions=['eu-west-1'],
            common_tags={'production': 'true'})

        roles = {}
        for role in ['web', 'db']:
            roles[role] = tags.get_instances(role=role)

        return roles

    env.roledefs = configure_roles()

    @roles('web')
    def restart_web():
        sudo('/etc/init.d/nginx restart')

    @roles('db')
    def restart_db():
        sudo('/etc/init.d/postgresql restart')

    def hostname():
        run('hostname')

    $ fab restart_db
    $ fab restart_web
    $ fab hostname --roles web
```
