"""
This module contains the Issue abstraction class which provides properties and
actions related to issues and bug reports.
"""
from typing import Set
from typing import Optional

from IGitt.Interfaces import IGittObject
from IGitt.Interfaces.User import User
from IGitt.Interfaces.Issue import Issue
from IGitt.Interfaces.Repository import Repository


class Organization(IGittObject):
    """
    Represents an organization on GitHub or GitLab.
    """
    @property
    def description(self) -> str:
        """
        Returns the description of the Organization.
        """
        raise NotImplementedError

    @property
    def billable_users(self) -> int:
        """
        Number of paying/registered users on the organization.
        """
        raise NotImplementedError

    @property
    def owners(self) -> Set[User]:
        """
        Returns the user handles of all admin users, usually the owner role.
        """
        raise NotImplementedError

    @property
    def masters(self) -> Set[User]:
        """
        Returns the user handles of all users able to manage members, usually
        the master role (sometimes no such role exists, then same as owners).
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        The name of the organization.
        """
        raise NotImplementedError

    @property
    def suborgs(self):
        """
        Returns the sub-organizations within this repository.
        """
        raise NotImplementedError

    @property
    def repositories(self) -> Set[Repository]:
        """
        Returns the list of repositories contained in this organization.
        """
        raise NotImplementedError

    def filter_issues(self,
                      state: Optional[str]='opened',
                      label: Optional[str]=None,
                      assignee: Optional[str]=None) -> Set[Issue]:
        """
        Filters the issues in the organization based on properties

        :param state: 'opened' or 'closed' or 'all'
        :param label: Label of the issue
        :param assignee: username of issue assignee
        :return: Set of Issue objects
        """
        raise NotImplementedError

    @property
    def issues(self) -> Set[Issue]:
        """
        Returns set of issue objects in this organization.
        """
        raise NotImplementedError
