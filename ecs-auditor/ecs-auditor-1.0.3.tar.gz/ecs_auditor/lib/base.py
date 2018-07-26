def get_landscape(region):
    """Takes the region and returns the correct landscape name

    Args:
        region (str): a AWS region name, such as 'eu-west-1'

    Returns:
        String

    """
    return {
        'us-east-1': 'na',
        'eu-central-1': 'eu',
        'eu-west-1': 'uk'
    }.get(region, 'eu')

def get_environment(env):
    return {
        'prod': 'production',
        'preprod': 'preprod',
        'production': 'production'
    }.get(env, 'preprod')
