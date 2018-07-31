from spell.api import base_client


USER_RESOURCE_URL = "feedback"


class FeedbackClient(base_client.BaseClient):
    def __init__(self, resource_url=USER_RESOURCE_URL, **kwargs):
        self.resource_url = resource_url
        super(FeedbackClient, self).__init__(**kwargs)

    def post_feedback(self, content):
        """Post feedback to the team.

        Keyword arguments:
        content -- the content of the feedback to post

        Returns:
        None
        """
        payload = {
            "content": content,
        }
        r = self.request("post", self.resource_url, payload=payload)
        self.check_and_raise(r)
