# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.
from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand
from serialbox.models import Pool
from random_flavorpack import models


class Command(BaseCommand):
    help = _(
        'Loads some example pools into the database.'
    )

    def handle(self, *args, **options):
        sp1 = Pool.objects.create(
            readable_name=_('Pharmaprod 20mcg Pills'),
            machine_name='00313000007772',
            active=True,
            request_threshold=1000
        )
        models.RandomizedRegion.objects.create(
            readable_name=_('Pharmaprod 20mcg Pills'),
            machine_name='00313000007772',
            start=239380,
            active=True,
            order=1,
            pool=sp1,
            min=1,
            max=999999999999
        )
