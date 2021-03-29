from commands.base_command import BaseCommand
import json


class Lists(BaseCommand):

    def __init__(self):
        description = 'Lists all tracked keywords.'
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):

        with open('watchlist.json', 'r') as d:
            watchlist = json.load(d)

        str = 'Here are all the tracked keywords.\n'

        for i in range(len(watchlist['watchlist'])):
            str += f'{i+1}. {" ".join(watchlist["watchlist"][i]["term"])} in {watchlist["watchlist"][i]["sub"]}\n'

        await message.channel.send(str)
