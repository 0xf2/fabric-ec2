from boto import ec2


def get_instances_for_tags(tags, ec2_regions=None, aws_key=None, aws_secret=None):
    """ Returns a list of hosts, matching the given tags/ec2_regions.
    """
    # Use default regions (taken from boto) if user didn't specify a list
    if not ec2_regions:
        ec2_regions = ['us-east-1', 'us-west-1', 'us-west-2',
                       'sa-east-1',
                       'eu-west-1',
                       'ap-southeast-1',
                       'ap-northeast-1']

    tag_filter = {}
    for key, val in tags.iteritems():
        tag_filter['tag:%s' % key] = val

    host_list = []
    for region in ec2_regions:
        conn = ec2.connect_to_region(region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret)
        reservations = conn.get_all_instances(None, tag_filter)
        for res in reservations:
            for instance in res.instances:
                if instance.public_dns_name != '':
                    # Terminated/stopped instances will not have a public_dns_name
                    host_list.append(instance.public_dns_name)
    return host_list


