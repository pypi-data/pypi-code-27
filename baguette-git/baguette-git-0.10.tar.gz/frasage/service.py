#-*- coding:utf-8 -*-
"""
| Module GIT which is responsible for the creation/deletion
| of the GIT repos/accounts/keys by listening for messages.

| If someone create/delete a repo/key fast,
| it might be posible that the delete is processed before
| but we don't give a shit about that (for the moment).

|The operations are idempotent.
"""
import farine.amqp
import farine.settings
import pyolite

class Frasage(object):
    """
    Service which contains the event loops to manage the GIT workflow:
    * delete-user
    * delete-organization
    * create-key
    * delete-key
    * create-repo
    * delete-repo
    * create-member
    * delete-member
    """
    def __init__(self):
        self.olite = pyolite.Pyolite(admin_repository=farine.settings.frasage['gitolite'])#pylint:disable=no-member

    @farine.amqp.consume(exchange='git', routing_key='delete-user')
    def delete_user(self, body, message):
        """
        Listen to the `exchange` git
        | and delete the user accordly to the messages.
        | Idempotent.

	:param body: the user's name to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.users.delete(body['user'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='delete-organization')
    def delete_organization(self, body, message):
        """
        Listen to the `exchange` git
        | and delete the organization accordly to the messages.
        | Idempotent.

	:param body: the organization's name to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.groups.delete(body['organization'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='create-key')
    def create_key(self, body, message):
        """
        Listen to the `exchange` git,
        | and create the user's key accordly to the message.
        | Idempotent.

	:param body: The message's content.
        :type body: dict
        :param message: The user and its key to create.
        :type message: kombu.message.Message
        :returns: The creation state
        :rtype: bool
	"""
        if body.get('user_creation'):
            user = self.olite.users.get_or_create(body['user'], key=body['key'])
        else:
            user = self.olite.users.get(body['user'])
        user.keys.append(body['key'])
        if body.get('organization_creation'):
            self.olite.groups.get_or_create(body['organization'])
            self.olite.groups.user_add(body['organization'], body['user'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='delete-key')
    def delete_key(self, body, message):
        """
        Listen to the `exchange` git
        | and delete the user's key accordly to the message.
        | Idempotent.

	:param body: The user and its key to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        user = self.olite.users.get(body['user'])
        user.keys.remove(body['key'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='create-repo')
    def create_repo(self, body, message):
        """
        Listen to the `exchange` git,
        | and create the repo accordly to the message.
        | Idempotent.

	:param body: The message's content.
        :type body: dict
        :param message: The repo's name to create.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.repos.get_or_create(body['repo'])
        self.olite.groups.get_or_create(body['organization'])
        self.olite.groups.repo_add(body['organization'], body['repo'], 'RW+')
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='delete-repo')
    def delete_repo(self, body, message):
        """
        Listen to the `exchange` git
        | and delete the repo accordly to the message.
        | Idempotent.

	:param body: The repo's name to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.repos.delete(body['repo'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='create-member')
    def create_member(self, body, message):
        """
        Listen to the `exchange` git,
        | and create the member accordly to the message.
        | Idempotent.

	:param body: The message's content.
        :type body: dict
        :param message: The member to create.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.groups.get_or_create(body['organization'])
        self.olite.groups.user_add(body['organization'], body['account'])
        message.ack()
        return True

    @farine.amqp.consume(exchange='git', routing_key='delete-member')
    def delete_member(self, body, message):
        """
        Listen to the `exchange` git
        | and delete the member accordly to the messages.
        | Idempotent.

	:param body: The member to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
	"""
        self.olite.groups.get_or_create(body['organization'])
        self.olite.groups.user_delete(body['organization'], body['account'])
        message.ack()
        return True
