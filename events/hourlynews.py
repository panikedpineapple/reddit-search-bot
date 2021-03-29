from events.base_event      import BaseEvent
from utils                  import get_channel

from datetime               import datetime
import json
import discord
import requests
import settings



class HourlyNews(BaseEvent):

    def __init__(self):
        interval_minutes = 60  # Set the interval for this event
        super().__init__(interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):

        with open('watchlist.json' , 'r') as d:
            watchlist = json.load(d)

        for trackers in watchlist['watchlist']:
            channel_id  = trackers['channel']
            term = trackers['term']
            sub = trackers['sub']

            c = client.get_channel(int(channel_id))

            if sub != '/all':
                payload = {
                    'q': ' '.join(term).strip(),
                    'limit': settings.LIMIT,
                    'sort': 'new',
                    'restrict_sr' : True,
                    't' : 'hour'
                }
                res = requests.get(url=f'{settings.REDDIT_ENDPOINT}/r{sub}/search.json', params=payload,
                                   headers={'User-Agent': 'MyApi/0.0.1'})
            else:
                payload = {
                    'q': ' '.join(term).strip(),
                    'limit': settings.LIMIT,
                    'sort': 'new',
                    't' : 'hour'
                }
                res = requests.get(url=f'{settings.REDDIT_ENDPOINT}/search.json', params=payload,
                                   headers={'User-Agent': 'MyApi/0.0.1'})
            # with open('data.json', 'w') as d:
            #     json.dump(res.json(), d)
            data = res.json()['data']['children']
            current_time = datetime.datetime.utcnow()

            m = discord.Embed(title="Recent news", description=f"Keyword(s): {','.join(term).title()}\n\n")

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

            await c.send(embed=m)




