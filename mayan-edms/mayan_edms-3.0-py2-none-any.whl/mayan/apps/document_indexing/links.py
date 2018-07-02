from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (
    icon_document_index_list, icon_index_main_menu, icon_index_setup,
    icon_rebuild_index_instances
)
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_edit,
    permission_document_indexing_delete, permission_document_indexing_rebuild,
)


def is_not_root_node(context):
    return not context['resolved_object'].is_root_node()


link_document_index_list = Link(
    args='resolved_object.pk', icon_class=icon_document_index_list,
    text=_('Indexes'), view='indexing:document_index_list',
)
link_index_main_menu = Link(
    icon_class=icon_index_main_menu, text=_('Indexes'),
    view='indexing:index_list'
)
link_index_setup = Link(
    icon_class=icon_index_setup, text=_('Indexes'),
    view='indexing:index_setup_list'
)
link_index_setup_list = Link(
    text=_('Indexes'), view='indexing:index_setup_list'
)
link_index_setup_create = Link(
    permissions=(permission_document_indexing_create,), text=_('Create index'),
    view='indexing:index_setup_create'
)
link_index_setup_edit = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Edit'),
    view='indexing:index_setup_edit',
)
link_index_setup_delete = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_delete,), tags='dangerous',
    text=_('Delete'), view='indexing:index_setup_delete',
)
link_index_setup_view = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Tree template'),
    view='indexing:index_setup_view',
)
link_index_setup_document_types = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Document types'),
    view='indexing:index_setup_document_types',
)
link_rebuild_index_instances = Link(
    icon_class=icon_rebuild_index_instances,
    description=_(
        'Deletes and creates from scratch all the document indexes.'
    ),
    permissions=(permission_document_indexing_rebuild,),
    text=_('Rebuild indexes'), view='indexing:rebuild_index_instances'
)
link_template_node_create = Link(
    args='resolved_object.pk', text=_('New child node'),
    view='indexing:template_node_create',
)
link_template_node_edit = Link(
    args='resolved_object.pk', condition=is_not_root_node, text=_('Edit'),
    view='indexing:template_node_edit',
)
link_template_node_delete = Link(
    args='resolved_object.pk', condition=is_not_root_node, tags='dangerous',
    text=_('Delete'), view='indexing:template_node_delete',
)
