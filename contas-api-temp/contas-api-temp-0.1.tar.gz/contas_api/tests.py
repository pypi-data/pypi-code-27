"""
Adiciona automaticamente o PEP8Test e o PyLint na chamada:
python manage.py test
"""
import subprocess
from test_pep8.tests import PEP8Test

# Testa o pylint nas contas_api
subprocess.call('pylint --load-plugins pylint_django contas_api/',
                shell=True)

# Testa o pylint nos usuários
subprocess.call('pylint --load-plugins pylint_django usuarios/',
                shell=True)

# Testa o pylint nos lancamentos
# Adiciona exceções a W0223, W0221, R0901, R0903
subprocess.call('pylint --load-plugins pylint_django \
                --disable=W0223,W0221,R0901,R0903 lancamentos/',
                shell=True)

# Testa o pylint nos lancamentos
# Adiciona exceções a W0221, R0901
subprocess.call('pylint --load-plugins pylint_django \
                --disable=W0221,R0901 contas/',
                shell=True)

__all__ = [
    'PEP8Test',
]
