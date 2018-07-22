# pyre-strict

"""
We use Pyre Check to prevent type errors. However, for Pyre Check to fail if
type declarations aren't "perfect", all files need to start with a "pyre-strict"
comment. This test checks that all Python files start with such a comment.
"""

import unittest
import os


class PyreStrictTest(unittest.TestCase):
    """
    Check that all relevant Python files have Pyre set to strict mode.
    """

    def test_strict_all_python_files(self) -> None:
        """
        Check that all relevant Python files have Pyre set to strict mode.
        """
        for directory, _directories, files in os.walk('.'):
            for file in files:
                path = os.path.join(directory, file)

                if self.path_can_safely_be_skipped(path):
                    continue

                with open(path) as current_file:
                    first_line: str = current_file.readline()

                    self.assertEqual(
                        first_line,
                        '# pyre-strict\n',
                        path + ' is not set to Pyre strict mode.',
                    )

    @staticmethod
    def path_can_safely_be_skipped(path: str) -> bool:
        """
        Make sure that we only check Python files that are in the present
        codebase.

        :param path:
        :return:
        """
        if not path.endswith('.py'):
            return True

        if './lib/' in path:
            # Prevent false positive in Scrutinizer.
            return True

        if './bin/activate_this.py' in path:
            # Prevent false positive in Scrutinizer.
            return True

        return False
