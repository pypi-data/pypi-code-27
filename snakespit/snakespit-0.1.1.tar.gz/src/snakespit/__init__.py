__version__ = '0.1.1'

import cleanlog
import requests
import tqdm

logger = cleanlog.ColoredLogger('snakespit')
BASE_URL = 'http://dohlee-bio.info:9193/%s/rule.smk'


def get_rules(rules):
    """
    TODO
    """
    rule_content = []
    warnings = []
    for rule in tqdm.tqdm(rules):
        rule = rule.strip('/')
        response = requests.get(BASE_URL % rule)

        if response.status_code == 200 and not response.text.startswith('404'):
            rule_content.append(response.text)
        else:
            warnings.append('No rule for %s.' % rule)

    for warning in warnings:
        logger.warning(warning)
    return '\n'.join(rule_content)
