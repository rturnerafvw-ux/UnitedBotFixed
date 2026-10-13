import asyncio
import logging
import os
import sqlite3
from datetime import datetime, timezone

import discord
import feedparser
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
POLL_MINUTES = max(5, int(os.getenv('POLL_MINUTES', '15')))
DB = sqlite3.connect('seen_posts.sqlite3')
DB.execute('CREATE TABLE IF NOT EXISTS seen (source TEXT, post_id TEXT, PRIMARY KEY(source,post_id))')
DB.commit()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def scan_feed(source, url, channel):
    if not url:
        return
    parsed = await asyncio.to_thread(feedparser.parse, url)
    if parsed.bozo and not parsed.entries:
        logging.warning('Feed unavailable: %s', source)
        return
    entries = list(reversed(parsed.entries[:10]))
    first_run = DB.execute('SELECT COUNT(*) FROM seen WHERE source=?', (source,)).fetchone()[0] == 0
    for entry in entries:
        post_id = entry.get('id') or entry.get('link')
        if not post_id or DB.execute('SELECT 1 FROM seen WHERE source=? AND post_id=?', (source, post_id)).fetchone():
            continue
        if not first_run:
            title = discord.utils.escape_markdown(entry.get('title', 'New announcement'))[:240]
            link = entry.get('link', '')
            embed = discord.Embed(title=title, url=link or None, description=f'New official {source} update.', color=0xF2B84B, timestamp=datetime.now(timezone.utc))
            embed.set_footer(text='UNITED Intelligence • Official source')
            await channel.send(embed=embed)
        DB.execute('INSERT OR IGNORE INTO seen VALUES (?,?)', (source, post_id))
        DB.commit()

@tasks.loop(minutes=POLL_MINUTES)
async def check_updates():
    channel = client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID)
    feeds = {
        'Facebook': os.getenv('FACEBOOK_FEED_URL', '').strip(),
        'YouTube': ('https://www.youtube.com/feeds/videos.xml?channel_id=' + os.getenv('YOUTUBE_CHANNEL_ID', '').strip()) if os.getenv('YOUTUBE_CHANNEL_ID', '').strip() else '',
    }
    for source, url in feeds.items():
        try:
            await scan_feed(source, url, channel)
        except Exception:
            logging.exception('Error checking %s', source)

@check_updates.before_loop
async def before_check():
    await client.wait_until_ready()

@client.event
async def on_ready():
    logging.info('Logged in as %s', client.user)
    if not check_updates.is_running():
        check_updates.start()

client.run(TOKEN)
