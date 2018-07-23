from longitude.models.sql import SQLCRUDModel


class RoleModel(SQLCRUDModel):

    table_name = 'longitude_permission_role'

    filters = {
        'is_superadmin': '_t.is_superadmin=%',
        'name': '_t.name=%'
    }
