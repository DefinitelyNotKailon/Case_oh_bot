import os
from twitchio.ext import commands
import json
import re
from dotenv import load_dotenv

load_dotenv()

class CaseOhBot(commands.Bot):
    def __init__(self):
        # Get credentials from environment variables
        token = os.getenv('BOT_TOKEN')
        channel = os.getenv('CHANNEL_NAME')
        
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.data_file = 'counter_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.counts = json.load(f)
        else:
            self.counts = {'total': 0}
            self.save_data()

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.counts, f)

    def get_ordinal(self, n):
        last_digit = n % 10
        last_two_digits = n % 100
        
        if 10 <= last_two_digits <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(last_digit, 'th')
        
        return f"{n}{suffix}"

    async def event_ready(self):
        print(f'Bot is ready! Connected to {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        pattern = r'case\s*o+h*'
        matches = re.finditer(pattern, message.content.lower())
        
        for match in matches:
            self.counts['total'] += 1
            matched_text = match.group()
            
            ordinal = self.get_ordinal(self.counts['total'])
            response = f"@{message.author.name} has just called lottness \"{matched_text}\" for the {ordinal} time!"
            
            await message.channel.send(response)
            self.save_data()

if __name__ == "__main__":
    bot = CaseOhBot()
    bot.run()
