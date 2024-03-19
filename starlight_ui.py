from decouple import config
from json import dump as json_dump
from interactions import (SlashContext, OptionType, Client, SlashCommand, slash_option, listen)
import os
import starlight_backend


@listen()
async def on_ready():
    """Lets the console know when the bot is online."""
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

    if not os.path.isfile(config("FILENAME")):
        starlight_backend.initialize_json(config("FILENAME"))


base_command = SlashCommand(
    name="starlight",
    description="Tracks leet code progress for Kat, Posi, Grey, and Rasp"
)


@base_command.subcommand(sub_cmd_name="help",
                         sub_cmd_description="Shows app description")
async def star_help(ctx: SlashContext):
    display_name = ctx.author.display_name
    leet_link = 'https://leetcode.com/problemset/'
    api_link = 'https://leetcodestats.cyclic.app/<username>'
    star_chips_img = 'https://media1.tenor.com/m/ALBBBwfJxfUAAAAd/yugioh-joey.gif'
    msg = (f"{display_name.title()}, it is time you become a leet coder.\n"
           f"You can find the leet code puzzles here, {leet_link}.\n\n"
           f"The rules are:\n"
           f"- No GPT for code, but you can ask GPT to explain concepts or data structures.\n"
           f"- You can look at the solution video when you want, but try not to, so you learn faster.\n\n"
           f"Each problem you complete will be worth a certain amount of __stars__.\n"
           f"This bot will view your completed problems automatically with this api: " 
           f"`{api_link}`\n"
           f"As for the amount of stars each problem is worth:\n"
           f"- Easy: 1 star\n- Medium: 3 stars\n- Hard: 5 stars\n\n"
           f"By default the quota will be 4 stars per week, but this can be adjusted as you get better.\n\n"
           f"Lastly, the bot will send you an alarm if you're under your expected star amount, based on your quota.\n"
           f"{star_chips_img}")

    await ctx.send(msg, ephemeral=True)


@base_command.subcommand(sub_cmd_name="status",
                         sub_cmd_description="Check your stars")
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def status(ctx: SlashContext, show_everyone=False):
    # Show number of solved problems and calculate stars
    user_id = str(ctx.author.id)
    data = starlight_backend.read_json(config("FILENAME"))
    leet_name = data[user_id]['leetcode_username']
    weekly_quota = data[user_id]['weekly_quota']
    stars_at_week_start = data[user_id]['stars_at_week_start']
    warning_message = data[user_id]['warning_message']
    warning_image = data[user_id]['warning_image_url']
    stats = starlight_backend.get_leetcode_stats(leet_name)
    msg = (f"``` ```"
           f"Username: {leet_name}\n- Stars: {stats['stars']}\n"
           f"- Stars This Week: {stats['stars'] - stars_at_week_start}\n"
           f"- Weekly Star Quota: {weekly_quota}\n"
           f"- Total Solved: {stats['totalSolved']}\n"
           f"- Easy Solved: {stats['easySolved']}\n- Medium Solved: {stats['mediumSolved']}\n"
           f"- Hard Solved: {stats['hardSolved']}\n"
           f"- Warning Message: {warning_message}\n"
           f"- Warning Image: {warning_image}\n"
           f"``` ```"
           )

    await ctx.send(msg, ephemeral=not show_everyone)


@base_command.subcommand(sub_cmd_name="all_status",
                         sub_cmd_description="Check everyone's stars")
async def all_status(ctx: SlashContext):
    user_id = ctx.author.id
    await ctx.send(user_id)


@base_command.subcommand(sub_cmd_name="update_warning_message",
                         sub_cmd_description="Update your warning message")
async def update_warning_message(ctx: SlashContext, message: str):
    user_id = ctx.author.id
    await ctx.send(user_id)


@base_command.subcommand(sub_cmd_name="update_warning_image",
                         sub_cmd_description="Update your warning image with an image url")
async def update_warning_gif_url(ctx: SlashContext, url: str):
    user_id = ctx.author.id
    await ctx.send(user_id)


@base_command.subcommand(sub_cmd_name="update_quota",
                         sub_cmd_description="Update your quota of stars required each week")
async def update_quota(ctx: SlashContext, starts: int):
    user_id = ctx.author.id
    await ctx.send(user_id)

if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()
