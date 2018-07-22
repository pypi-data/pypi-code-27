# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from re import compile, IGNORECASE, UNICODE

from buildok.statements.chdir import ChangeDir
from buildok.statements.mkdir import MakeDir
from buildok.statements.symlink import MakeSymlink
from buildok.statements.web import ViewWeb
from buildok.statements.google import GoogleSearch
from buildok.statements.duckduckgo import DuckDuckGoSearch
from buildok.statements.wikipedia import WikipediaSearch
from buildok.statements.github_search import GitHubSearch
from buildok.statements.shell import ShellExec
from buildok.statements.chmod import ChangeMod
from buildok.statements.chown import ChangeOwner
from buildok.statements.kill import KillProcess
from buildok.statements.copy import Copy
from buildok.statements.move import Move
from buildok.statements.remove import Remove
from buildok.statements.touch import Touch
from buildok.statements.edit_file import EditFile
from buildok.statements.install_pip import PipInstallPackage
from buildok.statements.install_npm import NpmInstallPackage
from buildok.statements.install import InstallPackage
from buildok.statements.uninstall import UninstallPackage
from buildok.statements.reinstall import ReinstallPackage
from buildok.statements.service_enable import EnableService
from buildok.statements.service_disable import DisableService
from buildok.statements.service_status import StatusService
from buildok.statements.service_start import StartService
from buildok.statements.service_stop import StopService
from buildok.statements.service_restart import RestartService
from buildok.statements.service_reload import ReloadService
from buildok.statements.listdir import ListDir
from buildok.statements.invoke import InvokeTopic
from buildok.statements.noop import Noop

from buildok.util.log import Log


class Statement(object):
    """Statement parser and launcher.

    Attributes:
        actions (frozen set): Set of all known statements and actions.
        statements    (list): List of all statements.
        ready         (bool): Setup flag to determine status.
    """

    __actions = {
        ChangeDir,        # Change current working directory.
        MakeDir,          # Make a directory or make recursive directories.
        MakeSymlink,      # Make a symlink for a target source
        ViewWeb,          # Open a link in default browser.
        GoogleSearch,     # Perform a Google search and open default browser.
        DuckDuckGoSearch, # Perform a DuckDuckGo search and open default browser.
        WikipediaSearch,  # Perform a Wikipedia search and open default browser.
        GitHubSearch,     # Open a GitHub search in default browser.
        ShellExec,        # Run a command in shell.
        ChangeMod,        # Change permissions on file or directory.
        ChangeOwner,      # Change owner and group on file or directory.
        Copy,             # Copy files from a given source to a given destination.
        Move,             # Move files from a given source to a given destination.
        Remove,           # Remove files from a given source.
        KillProcess,      # Send SIGTERM signal to a process.
        Touch,            # Create a new file.
        EditFile,         # Edit content of an existing file.
        PipInstallPackage,# Install Python packages.
        NpmInstallPackage,# Install Node.js packages.
        InstallPackage,   # Install new package software.
        UninstallPackage, # Uninstall package software.
        ReinstallPackage, # Reinstall package software.
        InvokeTopic,      # Invoke new topic from guide.
        Noop,             # No operation; nothing to do.
        EnableService,    # Enable service at boot time.
        DisableService,   # Disable service at boot time.
        StatusService,    # Get status of service.
        StartService,     # Start new service.
        StopService,      # Stop running service.
        RestartService,   # Restart running service.
        ReloadService,    # Reload service configuration.
        ListDir,          # List files and directories from directory.
    }

    statements = {}
    ready = False

    @classmethod
    def prepare(cls):
        """Statement initialization.

        Loops through all supported actions, validates and maps statements with
        actions.

        Returns:
            bool: True if statements are mapped successful.
        """

        Log.debug("Preparing to scan %d actions" % len(cls.__actions))
        for action in cls.__actions:
            if not callable(action):
                raise SystemExit("Expected action to be callable")
            Log.debug("Scanning action: %s" % action.parse_description())
            for line in action.parse_statements():
                exp = compile(line.strip(), IGNORECASE|UNICODE)
                cls.statements.update({exp: action})
                Log.debug("Updating known patterns: %s" % exp.pattern)
        if len(cls.statements) < len(cls.__actions):
            raise SystemExit("Unable to map statements to action")
        cls.ready = True
        Log.debug("All statements are scanned")

    @classmethod
    def find_statement(cls, stmt):
        """Lookup a statement.

        Returns:
            mixt: Statement if found, otherwise None.
        """

        return cls.statements.get(stmt)

    @classmethod
    def has_statement(cls, stmt):
        """Check whetever a statement exists.

        Returns:
            bool: True if statement is found.
        """

        return cls.find_statement(stmt) is not None

    @classmethod
    def get_statements(cls):
        """Statetements getter.

        Returns:
            iterator: A key-value itertator of all statements.
        """

        return cls.statements.iteritems()

    @classmethod
    def get_actions(cls):
        """Actions getter.

        Returns:
            list: All supported actions.
        """

        return cls.__actions
