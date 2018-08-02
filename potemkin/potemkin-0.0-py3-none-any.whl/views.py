from pyramid.view import view_config

import oauthlib.oauth1
import oauthlib.common
import webob


@view_config(
    route_name="ltilaunch_iframe", renderer="templates/ltilaunch_iframe.html.jinja2"
)
def ltilaunch_iframe(request):
    """The parent page containing the <iframe> LTI apps are launched within."""
    return {}


@view_config(
    route_name="ltilaunch_form", renderer="templates/ltilaunch_form.html.jinja2"
)
def lti_launch(request):
    """The LTI launch request form."""
    oauth_consumer_key = "Hypothesise3f14c1f7e8c89f73cefacdd1d80d0ef"

    fields = dict(
        oauth_consumer_key=oauth_consumer_key,
        tool_consumer_instance_guid="1",
        user_id="3",
        lis_person_name_full="Fred User",
        lis_person_name_family="",
        lis_person_name_given="",
        roles="Instructor,urn:lti:instrole:ims/lis/Administrator",
        context_id="87a38c9d",
        resource_link_id="747f*4eb3",
        lti_version="LTI-1p0",
    )

    request = oauthlib.common.Request(
        "https://example.com",  # The URL doesn't matter here.
        body=fields)
    oauth1_client = oauthlib.oauth1.Client(oauth_consumer_key)
    oauth_params = dict(oauth1_client.get_oauth_params(request))
    fields.update(
        dict(
            oauth_nonce=oauth_params["oauth_nonce"],
            oauth_timestamp=oauth_params["oauth_timestamp"],
            oauth_version=oauth_params["oauth_version"],
            oauth_signature_method=oauth_params["oauth_signature_method"],
        )
    )
    return dict(fields=fields)


@view_config(route_name="ltilaunch_sign", renderer="json")
def lti_sign(request):
    """Receive a form submission and return a signature of the form."""
    m = webob.multidict.MultiDict(request.params)
    lti_launch_url = m.pop("lti_launch_url")
    oauth1_client = oauthlib.oauth1.Client(
        request.params["oauth_consumer_key"],
        client_secret="2f3f8492ded6f45bc3698c8ec622d6a7c7f22f9112f1735b128d21d91aa5ea55bd5109e50afadd34e0dac4e953367828689516ea573fe5de580d71dd96f4b61f",
    )
    oauth_signature = oauth1_client.get_oauth_signature(
        oauthlib.common.Request(
            lti_launch_url,
            http_method="POST",
            body=m,
        )
    )
    return dict(oauth_signature=oauth_signature)
