from .sites import ambition_sites


class InvalidSiteError(Exception):
    pass


def get_site_id(name):
    """Expects sites list has elements of format
    (SITE_ID(int), site_name(char), site_long_name(char)).
    """
    try:
        return [site for site in ambition_sites if site[1] == name][0][0]
    except IndexError:
        try:
            return [site for site in ambition_sites if site[2] == name][0][0]
        except IndexError:
            site_ids = [site[1] for site in ambition_sites]
            site_names = [site[2] for site in ambition_sites]
            raise InvalidSiteError(f'Invalid site. Got \'{name}\'. Expected one of '
                                   f'{site_ids} or {site_names}.')
