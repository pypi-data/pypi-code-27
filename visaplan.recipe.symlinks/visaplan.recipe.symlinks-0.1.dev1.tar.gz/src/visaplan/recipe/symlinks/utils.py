# utils.py for visaplan.recipe.symlinks
from os import makedirs, symlink, readlink, unlink
from os.path import (normpath, abspath, relpath,
        exists, isdir, islink,
        )

from zc.buildout import UserError

__all__ = [
        'check_ternary_value', 'ternary_bool',
        'check_directory', 'check_symlink',
        'symlink_clone',
        ]


TRUE_VALUES = ('yes', 'true',  'on',  '1,' 'sure')
FALSE_VALUES = ('no', 'false', 'off', '0', 'nope')

DEFAULTS_MAP = {
        # create symbolic links to relative targets:
        'relative-links': 'no',
        # create links for every leaf:
        'link-leaves': 'no',
        }


def ternary_bool(val):
    """
    Convert the given textual value to a ternary boolean
    """
    val = val.strip().lower()
    if val in TRUE_VALUES:
        return True
    if val in FALSE_VALUES:
        return False
    if val == 'auto':
        return None
    raise ValueError("Boolean value or 'auto' expected; "
                     'got %(val)r'
                     % locals())

VALUES_MAP = {
        'yes': TRUE_VALUES,
        'no': FALSE_VALUES,
        'auto': ('auto',)
        }
def check_ternary_value(key,
        options,
        defaults_map=DEFAULTS_MAP,
        values_map=VALUES_MAP,
        **kwargs):
    """
    Check the given key for an allowed value and normalize it

    keyword arguments:

    allowed -- a list of keys of the values_map
    implemented -- a subset of <allowed>
        (a value might be allowed but not yet implemented)
    """
    val = options.get(key, None)
    if not val:
        if key in defaults_map:
            val = defaults_map[key]
        else:
            raise UserError("'%(key)s: a value is required!"
                            % locals())
    allowed = kwargs.pop('allowed', values_map.keys())
    implemented = kwargs.pop('implemented', allowed)
    for group in allowed:
        if val == group or val in values_map[group]:
            if group not in implemented:
                raise UserError("'%(key)s': Sorry, %(val)r "
                                'is not implemented yet.'
                                % locals())
            elif val != group:
                options[key] = group
            return group
    raise UserError("'%(key)s': value %(val)r is not allowed."
                    % locals())


def check_directory(dirname, **kwargs):
    """
    Check the existence of <dirname>, and assert it is not a non-directory

    Return True, if the directory needs to be created,
    and False, if it does exist already;
    if the given path exists and is not a directory, raise a UserError.
    """
    if not exists(dirname):
        return True
    if isdir(dirname):
        return False

    msg = []
    key = kwargs.pop('key', None)
    if key is not None:
        msg.append('%(key)s:' % locals())
    else:
        pkg = kwargs.pop('pkg', None) or kwargs.pop('package', None)
        if pkg is not None:
            msg.append('Error processing package %(pkg)s:'
                       % locals())
    msg.append("'%(dirname)s' exists but is not a directory!"
               % locals())
    if kwargs:
        msg.append('UNUSED ARGUMENTS: %(kwargs)r' % locals())
    raise UserError(' '.join(msg))


def check_symlink(linkname, target, **kwargs):
    """
    Check the existence of the symbolic link <linkname>;
    unlink it if it is a symlink pointing to another target.

    Return True, if the symlink needs to be (re)created;
    return False, if the symlink already exists with the given target;
    raise an error if <linkname> is a non-symlink filesystem object.
    """
    if not exists(linkname):
        return True
    if islink(linkname):
        if readlink(linkname) != target:
            unlink(linkname)
            return True
        return False

    msg = []
    pkg = kwargs.pop('pkg', None)
    if pkg:
        msg.append("Error processing package '%(pkg)s':"
                   % locals())
    msg.append("Error creating symbolic link "
               "to '%(target)s': '%(linkname)s' exists "
               "but is not a symbolic link!"
               % locals())
    if kwargs:
        msg.append('UNUSED ARGUMENTS: %(kwargs)r' % locals())
    raise UserError(' '.join(msg))


def symlink_clone(oriroot, cloneroot,
                  created,
                  relative=False,
                  **kwargs):
    """
    Create a symlink clone <cloneroot> of the tree rooted in <oriroot>:

    - cloneroot will be created, if it doesn't exist;
    - for each file in oriroot, a symbolic link will be created
      to the respective file in cloneroot;
    - for each subdirectory of oriroot, a symlink_clone will be created
      in cloneroot.
    """
    if relative:
        f = _symlink_clone_relative
    else:
        f = _symlink_clone_absolute
    return f(oriroot, cloneroot, created, **kwargs)


def _symlink_clone_absolute(oriroot, cloneroot, created, **kwargs):
    if not isdir(oriroot):
        raise ValueError('original %(oriroot)r is not a directory'
                         % locals())
    if check_directory(cloneroot, **kwargs):
        created(cloneroot)
        makedirs(cloneroot)
    for name in listdir(oriroot):
        orifull = join(oriroot, name)
        if isdir(orifull):
            _symlink_clone_absolute(orifull,
                                    join(cloneroot, name),
                                    created,
                                    **kwargs)
        else:
            clonefull = join(cloneroot, name)
            target = abspath(orifull)
            if check_symlink(clonefull, target, **kwargs):
                created(clonefull)
                symlink(target, clonefull)


def _symlink_clone_relative(oriroot, cloneroot, created, **kwargs):
    if not isdir(oriroot):
        raise ValueError('original %(oriroot)r is not a directory'
                         % locals())
    if check_directory(cloneroot, **kwargs):
        created(cloneroot)
        makedirs(cloneroot)
    for name in listdir(oriroot):
        orifull = join(oriroot, name)
        if isdir(orifull):
            _symlink_clone_relative(orifull,
                                    join(cloneroot, name),
                                    created,
                                    **kwargs)
        else:
            clonefull = join(cloneroot, name)
            target = relpath(orifull, cloneroot)
            if check_symlink(clonefull, target, **kwargs):
                created(clonefull)
                symlink(target, clonefull)
