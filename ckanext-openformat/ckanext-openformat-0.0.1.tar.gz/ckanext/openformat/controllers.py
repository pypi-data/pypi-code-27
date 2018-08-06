from ckan.controllers.package import PackageController

import logging
from urllib import urlencode
import datetime
import mimetypes
import cgi

from ckan.common import config
from paste.deploy.converters import asbool
import paste.fileapp

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.i18n as i18n
import ckan.lib.maintain as maintain
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.plugins as p
import ckan.lib.render

import requests
import mimetypes
from urlparse import urlparse
from os.path import splitext

from ckan.common import OrderedDict, _, json, request, c, response

log = logging.getLogger(__name__)

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin

class NewController(PackageController):
    def new_resource(self, id, data=None, errors=None, error_summary=None):
        ''' FIXME: This is a temporary action to allow styling of the
        forms. '''
        if request.method == 'POST' and not data:
            save_action = request.params.get('save')
            data = data or \
                clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(request.POST))))
                
            # patch to restrict file upload extension
            # ericsnth 06/08/2018 | ericsn.th@gmail.com

            ericsnth = {'action': 'filter'}
            ericsnth['format'] = str(data['format']).encode('ascii', 'ignore').lower()
            ericsnth['url'] = str(data['url']).encode('ascii', 'ignore').lower()
            ericsnth['upload'] = str(data['upload']).encode('ascii', 'ignore')[25:-2].lower()
            ericsnth['status'] = "accept"

            if ericsnth['upload'] == "" and ericsnth['url'] == "":
                abort(403, _('Berkas harus diisi !'))
            else:
                if ericsnth['url'] != "" and ericsnth['upload'] == "":
		    try:
                    	response = requests.get(ericsnth['url'])
                    	content_type = response.headers['content-type']
                    	extension = mimetypes.guess_extension(content_type)

                        if extension is None or extension == "":
                            parsed = urlparse(ericsnth['url'])
                            root, ext = splitext(parsed.path)
                            ericsnth['format'] = str(ext[1:]).lower()
		    except:
			parsed = urlparse(ericsnth['url'])
                        root, ext = splitext(parsed.path)
                        ericsnth['format'] = str(ext[1:]).lower()

                elif ericsnth['url'] == "" and ericsnth['upload'] != "":
                    temp = "http://ericsn.th/" + ericsnth['upload']
                    parsed = urlparse(temp)
                    root, ext = splitext(parsed.path)
                    ericsnth['format'] = str(ext[1:]).lower()

                else:
		    if ericsnth['url'][:4] != "http":
			try:
			    temp = "http://ericsn.th/" + ericsnth['url']
			    response = requests.get(temp)
                    	    content_type = response.headers['content-type']
                    	    extension = mimetypes.guess_extension(content_type)

                    	    if extension is None or extension == "":
                            	parsed = urlparse(temp)
                            	root, ext = splitext(parsed.path)
                            	ericsnth['format'] = str(ext[1:]).lower()
			except:
			    parsed = urlparse(temp)
                            root, ext = splitext(parsed.path)
                            ericsnth['format'] = str(ext[1:]).lower()

		    else:
                    	abort(403, _('Tidak diijinkan untuk menambah dua sumber sekaligus'))

            accepted = config.get('ericsnth.ckan.file_extension_allowed', 'csv xls xlsx doc docx pdf xml json').split(' ')
            if ericsnth['format'] in accepted:
                pass
            else:
                _format = ""
                for index, supe in enumerate(accepted):
                    if index == 0:
                        _format = supe
                    else:
                        _format = _format + ", " + supe
			
                abort(403, _('Format File yang diijinkan: ' + _format))

            # --------------------------------- end of config | ericsn.th@gmail.com
            # ericsnth 06/08/2018

            # we don't want to include save as it is part of the form
            del data['save']
            resource_id = data['id']
            del data['id']

            context = {'model': model, 'session': model.Session,
                       'user': c.user, 'auth_user_obj': c.userobj}

            # see if we have any data that we are trying to save
            data_provided = False
            for key, value in data.iteritems():
                if ((value or isinstance(value, cgi.FieldStorage))
                        and key != 'resource_type'):
                    data_provided = True
                    break

            if not data_provided and save_action != "go-dataset-complete":
                if save_action == 'go-dataset':
                    # go to final stage of adddataset
                    h.redirect_to(controller='package', action='edit', id=id)
                # see if we have added any resources
                try:
                    data_dict = get_action('package_show')(context, {'id': id})
                except NotAuthorized:
                    abort(403, _('Unauthorized to update dataset'))
                except NotFound:
                    abort(404, _('The dataset {id} could not be found.'
                                 ).format(id=id))
                if not len(data_dict['resources']):
                    # no data so keep on page
                    msg = _('You must add at least one data resource')
                    # On new templates do not use flash message

                    if asbool(config.get('ckan.legacy_templates')):
                        h.flash_error(msg)
                        h.redirect_to(controller='package',
                                      action='new_resource', id=id)
                    else:
                        errors = {}
                        error_summary = {_('Error'): msg}
                        return self.new_resource(id, data, errors,
                                                 error_summary)
                # XXX race condition if another user edits/deletes
                data_dict = get_action('package_show')(context, {'id': id})
                get_action('package_update')(
                    dict(context, allow_state_change=True),
                    dict(data_dict, state='active'))
                h.redirect_to(controller='package', action='read', id=id)

            data['package_id'] = id
            try:
                if resource_id:
                    data['id'] = resource_id
                    get_action('resource_update')(context, data)
                else:
                    get_action('resource_create')(context, data)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.new_resource(id, data, errors, error_summary)
            except NotAuthorized:
                abort(403, _('Unauthorized to create a resource'))
            except NotFound:
                abort(404, _('The dataset {id} could not be found.'
                             ).format(id=id))
            if save_action == 'go-metadata':
                # XXX race condition if another user edits/deletes
                data_dict = get_action('package_show')(context, {'id': id})
                get_action('package_update')(
                    dict(context, allow_state_change=True),
                    dict(data_dict, state='active'))
                h.redirect_to(controller='package', action='read', id=id)
            elif save_action == 'go-dataset':
                # go to first stage of add dataset
                h.redirect_to(controller='package', action='edit', id=id)
            elif save_action == 'go-dataset-complete':
                # go to first stage of add dataset
                h.redirect_to(controller='package', action='read', id=id)
            else:
                # add more resources
                h.redirect_to(controller='package', action='new_resource',
                              id=id)

        # get resources for sidebar
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'auth_user_obj': c.userobj}
        try:
            pkg_dict = get_action('package_show')(context, {'id': id})
        except NotFound:
            abort(404, _('The dataset {id} could not be found.').format(id=id))
        try:
            check_access(
                'resource_create', context, {"package_id": pkg_dict["id"]})
        except NotAuthorized:
            abort(403, _('Unauthorized to create a resource for this package'))

        package_type = pkg_dict['type'] or 'dataset'

        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'action': 'new',
                'resource_form_snippet': self._resource_form(package_type),
                'dataset_type': package_type}
        vars['pkg_name'] = id
        # required for nav menu
        vars['pkg_dict'] = pkg_dict
        template = 'package/new_resource_not_draft.html'
        if pkg_dict['state'].startswith('draft'):
            vars['stage'] = ['complete', 'active']
            template = 'package/new_resource.html'
        return render(template, extra_vars=vars)
