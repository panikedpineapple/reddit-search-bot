import discord
from commands.base_command import BaseCommand
import requests
import json
import settings
import datetime


class Topnews(BaseCommand):

    def __init__(self):

        description = 'Search Reddit for matching posts sorted by top posts.'
        params = []
        super().__init__(description,params)



    async def handle(self, params, message, client):
        full = message.content.split()[1:]
       # print(full)
        if full[-1].startswith('/'):
            sub_reddit = True
            ep = f"/r{full[-1]}/search"
            term = full[:-1]
            r = True
        else:
            sub_reddit = False
            ep = "/search"
            term = full
            r = False
      #  print(sub_reddit)
        payload = {
            'q' : ' '.join(term).strip(),
            'limit' : settings.LIMIT,
            'sort' : 'top'
        }
        if r:
            payload['restrict_sr'] = True
        # TO CHECK IF SORT BY TIME
        time_list = ['hour', 'day', 'month', 'year', 'all']
        if full[0].lower() in time_list:
            payload['t'] = full[0].lower()
            print(payload)
        res = requests.get(url=f'{settings.REDDIT_ENDPOINT}{ep}.json', params=payload, headers = {'User-Agent' : 'MyApi/0.0.1'})
        # with open('data.json', 'w') as d:
        #     json.dump(res.json(), d)
        data = res.json()['data']['children']
        current_time = datetime.datetime.utcnow()

        m = discord.Embed(title="Recent news", description=f"Keyword(s): {','.join(term).title()}\n\n")

        for post in data:
            time = datetime.datetime.utcfromtimestamp(int(post['data']['created_utc']))
            diff = (current_time - time).total_seconds()

            if diff < 3600:
                val = f"Created {round(diff//60)} Mins Ago."
            elif diff < 86400:
                val = f"Created {round(diff//3600)} hours ago."
            else:
                val = f"Created {round(diff//86400)} days ago."




          #  print(diff)
            title = post['data']['title']
            link = 'https://www.reddit.com'+ post['data']['permalink']
            desc = post['data']['selftext']
           # print(link)
            m.add_field(name = title[:256],
                        value=f'{val}\n'+desc[:100]+'...'+f'\n[Read More]({link})',
                        inline=False)


        await message.channel.send(embed = m)





