import discord
from commands.base_command import BaseCommand
import requests
import json
import settings
import datetime


class HourlyNews(BaseCommand):

    def __init__(self):

        description = 'Sends hourly posts for searched topics.'
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        full = message.content.split()[1:]
        # print(full)
        if full[-1].startswith('/'):
            sub_reddit = True
            ep = f"/r{full[-1]}/search"
            term = full[:-1]
        else:
            sub_reddit = False
            ep = "/search"
            term = full
        # print(sub_reddit)
        payload = {
            'q': ' '.join(term).strip(),
            'limit': settings.LIMIT,
            'sort': 'top',
            't': 'hour'
        }
        if sub_reddit:
            payload['restrict_sr'] = True

        # TO CHECK IF SORT BY TIME
        # time_list = ['hour', 'day', 'month', 'year', 'all']
        # if full[0].lower() in time_list:
        #     payload['t'] = full[0].lower()
        #     print(payload)
        res = requests.get(url=f'{settings.REDDIT_ENDPOINT}{ep}.json', params=payload,
                           headers={'User-Agent': 'MyApi/0.0.1'})
        # with open('data.json', 'w') as d:
        #     json.dump(res.json(), d)
        data = res.json()['data']['children']
        current_time = datetime.datetime.utcnow()

        m = discord.Embed(title="Recent news", description=f"Keyword(s): {','.join(term).title()}\n\n")

        # tracker data
        # ------------------------
        with open('watchlist.json', 'r') as d:
            watchlist = json.load(d)

        if sub_reddit:
            sub = full[-1]
        else:
            sub = '/all'

        watchlist['watchlist'].append({'channel': message.channel.id,
                                       'term': term,
                                       'sub' : sub})

        with open('watchlist.json', 'w') as d:
            json.dump(watchlist, d)
        # ----------------------------

        for post in data:
            time = datetime.datetime.utcfromtimestamp(int(post['data']['created_utc']))
            diff = (current_time - time).total_seconds()

            if diff < 3600:
                val = f"Created {round(diff // 60)} Mins Ago."
            elif diff < 86400:
                val = f"Created {round(diff // 3600)} hours ago."
            else:
                val = f"Created {round(diff // 86400)} days ago."

            # print(diff)
            title = post['data']['title']
            link = 'https://www.reddit.com' + post['data']['permalink']
            desc = post['data']['selftext']
            # print(link)
            m.add_field(name=title[:256],
                        value=f'{val}\n' + desc[:100] + '...' + f'\n[Read More]({link})',
                        inline=False)
        await message.channel.send('This keyword is now tracked. Hourly news will be send to this channel every hour.')
        await message.channel.send(embed=m)

