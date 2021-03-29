from commands.base_command import BaseCommand
import json


class Clear(BaseCommand):

    def __init__(self):
        description = 'Clears specified keyword.'
        params = ['number']
        super().__init__(description, params)

    async def handle(self, params, message, client):
        with open('watchlist.json', 'r') as d:
            watchlist = json.load(d)

        try:
            watchlist['watchlist'].pop(int(params[0])-1)
        except IndexError:
            await message.channel.send('The Key does not exist. Please type a number corresponding to the keyword.')
        else:
            with open("watchlist.json", 'w') as d:
                json.dump(watchlist,d)

            await message.channel.send('Keyword successfully removed.')
