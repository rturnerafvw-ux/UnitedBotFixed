# UNITED Intelligence — Duck Survival news bot

This is a starter bot, not a hosted or connected service. It checks configured RSS/Atom feeds and posts new entries to your UNITED Discord channel. It records existing entries on the first run without posting old news.

## Discord official announcements

Visit the official Duck Survival Discord and check its announcements channel for a **Follow** button. If available, choose Follow and select your UNITED news channel. This is Discord's native cross-server announcement feature; the custom bot cannot read a different server without being added there and given access. If Follow is unavailable, request permission from that server's administrators rather than scraping private messages.

## Facebook

The supplied Facebook share URL is **not** an RSS feed. Do not put it in `FACEBOOK_FEED_URL`. An authorized, reliable Facebook-to-RSS provider or approved Meta API integration must be established before Facebook updates can be automated. This starter does not scrape Facebook.

## Setup

1. Create a channel named `duck-survival-news` in UNITED.
2. In https://discord.com/developers/applications create an application, add a bot, and reset/copy its token. Never share the token publicly.
3. Under OAuth2 > URL Generator, select `bot` scope and permissions **View Channels**, **Send Messages**, and **Embed Links**. Use the generated invite URL to add it to UNITED.
4. Enable Developer Mode in Discord, right-click or long-press your news channel, and copy its channel ID.
5. Install Python 3.11+, then run `pip install -r requirements.txt`.
6. Copy `.env.example` to `.env` and fill in your token and channel ID. Optionally add a verified authorized feed URL.
7. Run `python bot.py` on an always-on server or hosting service. A running process is required for automatic updates.

## Limitations

The bot currently supports feed-based Facebook (only if a valid authorized feed exists) and YouTube (when an official channel exists). Official Discord announcements use the separate Follow feature if enabled. It does not monitor either source until connected. Feed checking occurs every 15 minutes by default; new posts may arrive later. SQLite tracks seen entries to avoid reposts. If no feeds are configured, it will log in but post nothing.
