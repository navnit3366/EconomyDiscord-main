import discord
#import keep_alive
import asyncio 
import os
from discord.ext import commands
import random 
import string 
import sqlite3
import time 

conn = sqlite3.connect('bank.db')
cursorObj = conn.cursor()


        
def get_bank(userID):
    conn = sqlite3.connect('bank.db')
    cursorObj = conn.cursor()
    cursor = cursorObj.execute("SELECT ID, MONEY FROM bank")
    for row in cursor:
        if userID in row:
            return(round(row[1]))
    conn.commit()

def update_bank(userID, amount):
    cursorObj.execute(f'UPDATE bank SET MONEY = MONEY + {amount} where ID = {userID}')
    conn.commit()

def make_bank(userID):
    print(f"Making Banl for {userID}")
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS bank (ID INT PRIMARY KEY,MONEY INT);")
    except Exception as e:
        print(e)
    if get_bank(userID) is None:
        try:
            conn.execute(f"INSERT INTO bank (ID, MONEY)  VALUES ({int(userID)}, 0 );")
            conn.commit()
        except Exception as e:
            print(e)
    


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.command(hidden=True)
    async def makeall(self, ctx):
        if ctx.author.id==386837370466598914:
            for a in self.bot.get_all_members():
                if not a.bot:
                    if a.id is not None:
                        make_bank(str(a.id))


    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in as {}".format(self.bot.user))

    @commands.command()
    @commands.cooldown(1, 30.0, commands.BucketType.user)
    async def flipcoin(self, ctx, bet:int):
        if bet>get_bank(ctx.author.id):
            embed=discord.Embed(description='You can only bet what you have, Dumb.', color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        if bet<=0:
            embed=discord.Embed(description="Will you stop trying these dirty tricks on me?", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        if bet>0 and bet<get_bank(ctx.author.id):
            coinsides=["Heads", "Tails"]
            coinside=["Heads", "Tails"]
            usersside=random.choice(coinsides)
            coinsides.remove(usersside)
            Compside=coinsides[0]
            embed=discord.Embed(description=f"You chose {usersside} and bet {bet} coins. Flipping coin...", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
            win=random.choice((usersside, Compside))
            await asyncio.sleep(3)
            if win==usersside:
                embed=discord.Embed(description=f'You won! You get {bet} coins.', color=discord.Colour.dark_gold())
                await ctx.send(embed=embed)
                update_bank(ctx.author.id, bet)
            elif win==Compside:
                embed=discord.Embed(description=f"You suck at this. You just lost {bet} coins. What a noob!", color=discord.Colour.dark_gold())
                await ctx.send(embed=embed)
                update_bank(ctx.author.id, bet*-1)

    @flipcoin.error
    async def flipcoin_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(description="BRUH! Atleast tell the amount you want to bet or stop using this bot.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(description="You are gonna lose all your money betting. Wait {:.2f} seconds".format(error.retry_after), color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

            await ctx.send()
        else:
            raise error
    
    @commands.command()
    async def give(self, ctx, member:discord.Member, coins:int):
        make_bank(str(ctx.author.id))
        make_bank(str(member.id))
        if member==ctx.message.author:
            embed=discord.Embed(description="You can't give coins to yourself idiot!", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

        elif coins>get_bank(ctx.author.id):
            embed=discord.Embed(description="You can't give more than what you have. Someone teach this noob some maths.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

            
        elif coins<0:
            embed=discord.Embed(description="Don't try your dirty tricks on me.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

        else:
            update_bank(ctx.author.id, coins*-1)
            update_bank(member.id, coins)
            embed=discord.Embed(description=f"You gave {member.name} {coins} coins!", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

           

    @commands.command()
    async def bal(self, ctx,member:discord.Member=None):
        make_bank(str(ctx.author.id))
        if member==None:
            money=str(get_bank(ctx.author.id))
            embed=discord.Embed(description=f"{ctx.author.name}'s balance: **{money}**", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            money=str(get_bank(member.id))
            embed=discord.Embed(description=f"{member.name}'s balance: **{money}**", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

    @bal.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed=discord.Embed(description="I can't find that user. Please ping them and make sure they exist.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            raise error
    
    @commands.command()
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    async def search(self, ctx):
        make_bank(str(ctx.author.id))
        embed=discord.Embed(description="Where do you want to search? Bank, Discord, Car", color=discord.Colour.dark_gold())
        await ctx.send(embed=embed)
        def check(message):
            return message.author == ctx.author
        try:
            Tosearch = await self.bot.wait_for('message',timeout=45.0, check=check)
        except asyncio.TimeoutError:
            embed=discord.Embed(description="You did not tell where to search in time.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        earned=random.randint(30, 80)
        if Tosearch.content.lower()=="bank":
            update_bank(ctx.author.id, earned)
            embed=discord.Embed(description=f"You searched in the bank and got {earned} coins. Did you just rob the bank?", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        elif Tosearch.content.lower()=="discord":
            update_bank(ctx.author.id, earned)
            embed=discord.Embed(description=f"Someone sent you {earned} coins in your DM. Check your DMs more often.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        elif Tosearch.content.lower()=="car":
            update_bank(ctx.author.id, earned)
            embed=discord.Embed(description=f"Bruh do you think you are in GTA? You took {earned} coins from someone's car", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="Type a proper place to search next time.", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(description='Bruh, wait {:.2f} seconds before searching again.'.format(error.retry_after), color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx): 
        make_bank(str(ctx.author.id))
        moneyD=random.randint(200, 800)
        embed=discord.Embed(description=f"Congrats! You have received {moneyD} coins as your daily gift!", color=discord.Colour.dark_gold())
        await ctx.send(embed=embed)
        update_bank(ctx.author.id, moneyD)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a=time.strftime("Please wait %H Hours, %M Mins and %S seconds", time.gmtime(error.retry_after))
            embed=discord.Embed(description=a, color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            raise error
    @commands.command()
    async def leaderboard(self, ctx):
        cursor=cursorObj.execute("""SELECT * FROM bank
        ORDER BY MONEY DESC""")
        counter = 0 
        top10=[]
        top=[]
        for row in cursor:
            counter += 1 
            winner=self.bot.get_user(row[0])
            top10.append(f"{counter}. {str(winner)} Coins: {round(row[1])}")
            #await ctx.send(f"{counter}. {winner.name} Coins: {row[1]}")
            if counter == 10:
                break
        #des=(top10,sep='\n')
        embed=discord.Embed(title=f"**{ctx.guild.name} leaderboard:**", description='\n'.join(top10), color=discord.Colour.dark_gold())
        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.cooldown(1, 30.0, commands.BucketType.user)
    async def beg(self, ctx):
        donate=random.randint(0,25)
        update_bank(ctx.author.id, donate)
        embed=discord.Embed(description=f"Someone donated you {donate} coins!", color=discord.Colour.dark_gold())
        await ctx.send(embed=embed)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'You wanna become a professional beggar or something? Try again after {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 30.0, commands.BucketType.user)
    async def rob(self, ctx, member:discord.Member=None):
        make_bank(str(ctx.author.id))
        make_bank(str(member.id))
        if member==None:
            embed=discord.Embed(description="Bruh who are you gonna rob?", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)

        elif member==ctx.author:
            embed=discord.Embed(description="Do you really wanna rob yourself?", color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            if get_bank(ctx.author.id)<500:
                embed=discord.Embed(description="You need atleast 500 coins to rob someone. Haha poor guy trying to rob someone.", color=discord.Colour.dark_gold())
                await ctx.send(embed=embed)

            if get_bank(ctx.author.id)>500:
                if get_bank(member.id)<500:
                    embed=discord.Embed(description="They must have atleast 500 coins so you can rob them.", color=discord.Colour.dark_gold())
                    await ctx.send(embed=embed)

                elif get_bank(member.id)>500:
                    roborno=random.randint(0,100)
                    if roborno<40:
                        loose=round(random.randint(0,100))
                        if loose<2:
                            lose=get_bank(ctx.author.id)
                            update_bank(ctx.author.id, lose*-1)
                            embed=discord.Embed(description="You were caught redhanded. All your coins were taken lmao", color=discord.Colour.dark_gold())
                            await ctx.send(embed=embed)
                        if loose>50:
                            lose=10/100*get_bank(ctx.author.id)
                            update_bank(ctx.author.id, lose*-1)
                            embed=discord.Embed(description=f"Someone saw you trying to rob but you gave them {lose} coins and they let you go", color=discord.Colour.dark_gold())
                            await ctx.send(embed=embed)
                        if loose<50 and loose>40:
                            lose=30/100*get_bank(ctx.author.id)
                            update_bank(ctx.author.id, lose*-1)
                            embed=discord.Embed(description=f"A police officer caught you robbing. You paid {coins} coins as fine.", color=discord.Colour.dark_gold())
                            await ctx.send(embed=embed)
                    if roborno>40:
                        if roborno<41:
                            lose=round(get_bank(ctx.author.id))
                            update_bank(ctx.author.id, lose)
                            update_bank(member.id, lose*-1)
                            embed=discord.Embed(description=f"You stole everything HAHA. You got {lose} coins.", color=discord.Colour.dark_gold())
                            await ctx.send(embed=embed)
                        if roborno>41 and roborno<80:
                            lose=round(10/100*get_bank(ctx.author.id))
                            update_bank(ctx.author.id, lose)
                            update_bank(member.id, lose*-1)
                            embed=discord.Embed(description=f"You got yourself {lose} coins", color=discord.Colour.dark_gold())
                            await ctx.send(embed=embed)
                    if roborno>80:
                        lose=round(50/100*get_bank(ctx.author.id))
                        embed=discord.Embed(description=f"You stole a large portion and got {lose} coins", color=discord.Colour.dark_gold())
                        await ctx.send(embed=embed)
                        update_bank(ctx.author.id, lose)
                        update_bank(member.id, lose*-1)
    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(description="I am gonna rob you if you don't stop noob. Wait {:.2f}s".format(error.retry_after), color=discord.Colour.dark_gold())
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 604800.0, commands.BucketType.user)
    async def weekly(self, ctx): 
        moneyD=random.randint(2500, 5000)
        await ctx.send(f"Congrats! You have received {moneyD} coins as your weekly gift!")
        update_bank(ctx.author.id, moneyD)
    @weekly.error
    async def weekly_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a=time.strftime("Please wait %D, %H Hours, %M Mins and %S seconds", time.gmtime(error.retry_after)) 
            await ctx.send(a)
        else:
            raise error
    



    


def setup(bot):
    bot.add_cog(Currency(bot))
      
    



      