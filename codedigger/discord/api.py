import requests
from user.exception import ValidationException
from .models import DiscordWebhook


def execute_webhook(webhook: DiscordWebhook, embeds: list, *args, **kwargs):
    """
        :param webhook: object of discord webhook model
        :param embeds: array of up to 10 embed objects 

        This function will POST embeds to given webhook. 
    """
    # Ref: https://discord.com/developers/docs/resources/webhook#execute-webhook
    # Ref: https://discord.com/developers/docs/resources/channel#embed-object

    url = "https://discord.com/api/webhooks/{}/{}".format(
        webhook.webhook_id, webhook.webhook_token)
    headers = {"Content-Type": "application/json"}
    params = {"embeds": embeds}
    response = requests.post(url, headers=headers, json=params)

    if response.status_code != 204:
        raise ValidationException(response.content)
