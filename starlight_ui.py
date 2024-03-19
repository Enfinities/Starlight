from decouple import config
from interactions import (SlashContext, OptionType, Client, SlashCommand, slash_option, listen)
import os


@listen()
async def on_ready():
    """Lets the console know when the bot is online."""
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


base_command = SlashCommand(
    name="starlight",
    description="Tracks leet code progress for Kat, Posi, Grey, and Rasp"
)


@base_command.subcommand(sub_cmd_name="help",
                         sub_cmd_description="Shows app description")
async def star_help(ctx: SlashContext):
    display_name = ctx.author.display_name
    leet_link = 'https://leetcode.com/problemset/'
    msg = (f"{display_name.title()}, it is time you become a leet coder.\n"
           f"You can find the leet code puzzles here, {leet_link}.\n"
           f"The rules are:\n"
           f"- No GPT for code, but you can ask GPT to explain concepts or data structures.\n"
           f"- You can look at the solution video when you want, but try not to, so you learn faster.\n\n"
           f"Each problem you complete will be worth a certain amount of __stars__.\n"
           f"This bot will view your completed problems automatically with this api: " 
           "`https://leetcodestats.cyclic.app/<username>`\n"
           f"As for the amount of stars each problem is worth:\n"
           f"- Easy: 1 star\n- Medium: 3 stars\n- Hard: 5 stars\n\n"
           f"By default the quota will be 4 stars per week, but this can be adjusted as you get better.\n\n"
           f"Lastly, the bot will send you an alarm if you're under your expected star amount, based on your quota."
           f"https://i.ytimg.com/vi/2whikHH9Jpw/hqdefault.jpg"
    )

    await ctx.send(msg, ephemeral=True)


@base_command.subcommand(sub_cmd_name="status",
                         sub_cmd_description="Check your stars")
async def status(ctx: SlashContext):
    pass


async def all_status(ctx: SlashContext):
    pass


async def update_warning_message(ctx: SlashContext, message: str):
    pass


async def update_warning_gif_url(ctx: SlashContext, url: str):
    pass


async def update_quota(ctx: SlashContext, starts: int):
    pass

if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()
