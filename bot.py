import os, sys
from random import choice
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from discord.ext import commands
from time import sleep




# Handle Environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PERMISSIONS = os.getenv('PERMISSIONS')
CHANNEL_ID = 725134189652869270

class FileUploaderBot(Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Channel with ID {CHANNEL_ID} not found.")
            await self.close()
            return
        upload_Q = parse_files()
        print(os.listdir('.'))
        # Upload files from the designated folder
        for file in upload_Q:
            if os.path.isfile(file):
                try:
                    await channel.send(file=File(file))
                    print(f"Uploaded: {file}")
                except Exception as e:
                    print(f"Failed to upload {file}: {e}")
        sleep(3)
        print('SUCCESS!!')
        # Logout the bot after uploading files
        await self.close()


def parse_files() -> list[str]:
    os.chdir('output')
    files = os.listdir()
    parsed_files = []
    for file in files:
        parsed_files.append(file)
    print(f'Files parsed for bot: {parsed_files}')
    return parsed_files

def main() -> None:
    if not os.path.exists('output'):
        print('Error reading output folder..')
    else:
        intents = Intents.default()
        bot = FileUploaderBot(intents=intents)
        bot.run(TOKEN)

if __name__ == '__main__':
    main()
