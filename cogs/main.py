import discord, random, asyncio, datetime
from discord.ext import commands,tasks
from discord import app_commands
from typing import Optional


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        number = random.randint(30, 60)
        
        if message.author == self.bot.user:
            return
        if message.content == "帥哥":
            await asyncio.sleep(number)
            await message.channel.send("🚬")

   
    @app_commands.command(name = "add", description = "計算")
    @app_commands.describe(a = "輸入數字", b = "輸入數字")
    async def add(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"Total: {a + b}")

   
    @app_commands.command(name="delete", description="刪除聊天紀錄")
    @app_commands.describe(n="輸入要刪的句數")
    async def delete(self, interaction, n: int):
        await interaction.response.send_message(content="已刪除成功", ephemeral=True)
        await interaction.channel.purge(limit=n)
        
   
    @app_commands.command(name ="say" ,description="我代替你說話")
    @app_commands.describe(a="我幫你說")
    async def say(self, interaction, a: str):
        await interaction.response.send_message(content="<3", ephemeral=True)
        await interaction.channel.send(a)

    
    @app_commands.command(name ="repeat" ,description="重複你說的話")
    @app_commands.describe(b="我重複你說")
    async def repeat(self, interaction, b: str):
        await interaction.response.send_message(b)
    
    
    @app_commands.command(name="guess", description="終極密碼")
    async def guess(self, interaction:discord.Interaction):

        global lowernumber
        global highernumber

        lowernumber = 1
        highernumber = 100

        number = random.randint(lowernumber, highernumber)

        await interaction.response.send_message("1-100選一個數字 (輸入0結束) ")

        for i in range(0, 100):
            a = 1
            response = await self.bot.wait_for("message",check=lambda m: m.channel == interaction.channel)

            try:
                guess = int(response.content)

            except ValueError:
                await interaction.channel.send("輸入數字")
                a = 0

            if guess == 0:
                await interaction.channel.send("結束")
                break

            if guess == number:
                await interaction.channel.send("猜對了")
                break

            if a != 0:
                if guess == lowernumber or guess == highernumber:
                    await interaction.channel.send("選取範圍內的數字")
                    await interaction.channel.send(f"比 {lowernumber} 大，比 {highernumber} 小")

            if guess > highernumber or guess < lowernumber and guess != 0:
                await interaction.channel.send("選取範圍內的數字")
                await interaction.channel.send(f"比 {lowernumber} 大，比 {highernumber} 小")

            if lowernumber < guess < highernumber:

                if guess < number:
                    lowernumber = guess
                    await interaction.channel.send(f"比 {lowernumber} 大，比 {highernumber} 小")

                if guess > number:
                    highernumber = guess
                    await interaction.channel.send(f"比 {lowernumber} 大，比 {highernumber} 小")

    async def button_callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        members = guild.members
        random_member = random.choice(members)
        await interaction.channel.send(f"{random_member.mention}被選中了!")
        await interaction.message.delete()
        
    @app_commands.command(name = "choose", description = "是誰?")
    async def gay(self, interaction: discord.Interaction):
        view = discord.ui.View()
        button = discord.ui.Button(
            label = "是誰?",
            style = discord.ButtonStyle.red
        )
        # Button 連接回呼函式
        button.callback = self.button_callback
        # 將 Button 添加到 View 中
        view.add_item(button)
        await interaction.response.send_message(content="是誰?", view = view)

class TaskTimes(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.every_hour.start()

    @tasks.loop(hours=1)
    async def every_hour(self):
        channel = self.bot.get_channel(1224746470930907279)
        current_hour = datetime.datetime.now().hour
        embed = discord.Embed(
            title=f"【{current_hour}】了",
            color=discord.Color.random()
        )
        await channel.send(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))

