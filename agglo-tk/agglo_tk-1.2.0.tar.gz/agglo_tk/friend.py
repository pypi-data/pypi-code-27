############################################################################
##
## Copyright (C) 2025 Plaisic and/or its subsidiary(-ies).
## Contact: eti.laurent@gmail.com
##
## This file is part of the Agglo project.
##
## AGGLO_BEGIN_LICENSE
## Commercial License Usage
## Licensees holding valid commercial Agglo licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Plaisic.  For licensing terms and
## conditions contact eti.laurent@gmail.com.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## In addition, the following conditions apply:
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in
##       the documentation and/or other materials provided with the
##       distribution.
##     * Neither the name of the Agglo project nor the names of its
##       contributors may be used to endorse or promote products derived
##       from this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
## AGGLO_END_LICENSE
##
############################################################################


import inspect


class AtkNotFriendError(Exception):
    pass


def _is_method_defined(apy_class, as_method_name):
    b_Res = False
    
    # TODO a implementer
    # Iterate on all classes from which class asking for af_method inherits
    # for py_current_class in inspect.getmro(af_method.im_class):
        # # If method is in current class method list
        # b_Res = b_Res or (as_method_name in py_current_class.__dict__) 
            
    return b_Res

    
def _add_public_method(apy_class_priv, af_private_method, als_friends, as_public_method_name):

    def public_method(*args, **kwargs):
        py_stack = inspect.stack()
        s_calling_class_name = py_stack[1][0].f_locals["self"].__class__.__name__
        
        # If calling class is registered as a private method friend
        if (s_calling_class_name in public_method._ls_friends):
            # Call private method
            return public_method._f_private_method(*args, **kwargs)
        else:
            # Raise not friend exception
            message = s_calling_class_name + " is not allowed to call " + \
                      str(public_method._f_private_method) + " known as " + \
                      public_method._s_public_method_name
            raise AtkNotFriendError(message)

    public_method._f_private_method = af_private_method
    public_method._ls_friends = als_friends
    public_method._s_public_method_name = as_public_method_name
    setattr(apy_class_priv, as_public_method_name, public_method)

    
def has_friends(apy_class):
    ls_private_method = []
    
    # Iterate on all methods of apy_class
    for s_current_method_name, f_current_method in apy_class.__dict__.iteritems():
        # If current method has declared friends
        if hasattr(f_current_method, "_map_friends"):
            ls_private_method.append(f_current_method)
    
    # Iterate on methods with friends
    for f_current_private_method in ls_private_method:
        # Iterate on all public mnames defined for current private method
        for s_public_method_name in f_current_private_method._map_friends:
            # If public method already exist
            if (_is_method_defined(apy_class, s_public_method_name)):
                # Raise already used exception
                # TODO
                pass
            else:
                # Add a public method, with authorization for friends only
                _add_public_method(apy_class, f_current_private_method, 
                                   f_current_private_method._map_friends[s_public_method_name], 
                                   s_public_method_name)
    
    return apy_class

# TODO option pour autoriser l'heritage du friend
# TODO bug si self n'et pas friend mais utilise une method de sa classe mere qui est friend
def friend(as_friend_class_name, as_public_method_name=None):
    def make_friend(af_private_method):
        s_public_method_name = as_public_method_name
        
        # If method does not have a friends class set defined
        # (it could if the method has another friend)
        if not hasattr(af_private_method, "_map_friends"):
            # Create _map_friends attribute
            af_private_method._map_friends = {}

        # If user has not specified public method name
        if (s_public_method_name is None):
            # Public method name equals private method name, without heading _
            s_public_method_name = af_private_method.__name__
            s_public_method_name = s_public_method_name[0].replace('_', '') + s_public_method_name[1:]
            s_public_method_name = s_public_method_name[0].replace('_', '') + s_public_method_name[1:]
            
        # Add as_friend_class_name as friend of method
        af_private_method._map_friends.setdefault(s_public_method_name, []).append(as_friend_class_name)
        
        # Decorated method is a plain private method: when private 
        # method is called by user, no special treatment should be done
        return af_private_method
        
    return make_friend
    