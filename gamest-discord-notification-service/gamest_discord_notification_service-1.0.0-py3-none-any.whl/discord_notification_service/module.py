import requests

from gamest.errors import InvalidConfigurationError
from gamest.plugins import NotificationService

class DiscordNotificationService(NotificationService):
    def __init__(self, application):
        super().__init__(application)
        self.webhook_url = self.config.get('DiscordNotificationService', 'webhook_url', fallback=None)
        self.user_name = self.config.get('DiscordNotificationService', 'user_name', fallback=None)

        if not self.webhook_url:
            raise InvalidConfigurationError("Webhook URL must be set for discord notifier plugin.")

        if not self.user_name:
            raise InvalidConfigurationError("User name must be set for discord notifier plugin.")

        self.discord_id = self.config.get('DiscordNotificationService', 'discord_id', fallback=None)
        self.user_name_for_messages = '<@{}>'.format(self.discord_id) if self.discord_id else self.user_name

        self.logger.debug("DiscordNotificationService initialized."
            "\n\twebhook_url: %r"
            "\n\tuser_name: %r"
            "\n\tdiscord_id: %r",
            self.webhook_url, self.user_name, self.discord_id)

    def notify(self, msg):
        self.logger.debug("Notify called.")
        data = { 'content' : msg.format(user_name=self.user_name_for_messages) }
        for url in self.webhook_url.splitlines():
            r = requests.post(url, data=data)
        try:
            r.raise_for_status()
        except:
            self.logger.exception("Failed to send Discord notification.")
