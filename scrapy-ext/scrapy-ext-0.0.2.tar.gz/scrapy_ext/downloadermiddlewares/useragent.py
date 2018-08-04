import random
from ..ua_list import UA_LIST


class RandomUserAgentMiddleware(object):

    @staticmethod
    def process_request(request, spider):
        ua = random.choice(UA_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
            # this is just to check which user agent is being used for request
            spider.logger.debug(
                'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request)
            )
