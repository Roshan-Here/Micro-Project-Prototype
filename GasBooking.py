import asyncio

import random
import pymongo
from Config import Setup
import pyromod.listen
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup ,ReplyKeyboardRemove


Mango = pymongo.MongoClient(Setup.MONGO_URL)
db = Mango.Mango.newuserdetails

LeosBot = Client(name="GasBooking app",api_id=Setup.api_id,api_hash=Setup.api_hash)

@LeosBot.on_message(filters.command("start") & ~filters.group)
async def main(bot,msg):
    START=f"select an option :)"
    button = ReplyKeyboardMarkup([
            ["New User!!"],
            ["Login!!"],
            ["Admin!!"]
            ],resize_keyboard=True)
    await bot.send_message(chat_id=msg.chat.id,text=START,reply_markup=button)
    await asyncio.sleep(15)


@LeosBot.on_message(filters.regex("New User!!"))
async def acc(bot, msg):
    randomgasid = random.randint(1000,9999)
    newbie =msg.from_user.id
    x = await bot.send_message(newbie,text=f"closing keyboad...",reply_markup=ReplyKeyboardRemove())
    await x.delete()
    name = await LeosBot.ask(newbie, f"Send me your name:")
    print(name.text)
    address = await LeosBot.ask(newbie, "Giv me your address>>>")
    print(address.text)
    rationCC = await LeosBot.ask(newbie, "Giv Your Ration Card NO:")
    print(rationCC.text)
    checkrationcard = db.find({"rationCard":rationCC})
    if checkrationcard:
        await bot.send_message(newbie,f"Ration card already registered")
    else:
        # Check if ratioCC exist in db if yes already registerd Card :(
        phoneno = await LeosBot.ask(newbie, "Giv me your Phone No ")
        print(phoneno.text)
        Text = f"""
    your name is {name.text} :)
    Your address : {address.text}
    
    Your RationId : {rationCC.text}
    phone no : {phoneno.text}
        
    if details are wrong just press /start :)
    #NB not yet added update option :)
    """

        await bot.send_message(newbie,Text)
        useid = f"Gas#{randomgasid}"
        await bot.send_message(newbie,f"your Userid : {useid}")
        loginPass = await LeosBot.ask(newbie,f"Giv a new login pass :")
        print(loginPass.text)
        data = {
            'name': name.text,
            'rationCard': rationCC.text,
            'address': address.text,
            'phone': phoneno.text,
            'userid': useid,
            'loginpass': loginPass.text
        }
        wow = db.insert_one(data)
        print(wow)
        await bot.send_message(newbie,f"Account created Sucessfully :)")

@LeosBot.on_message(filters.regex("Login!!"))
async def loginview(bot,msg):
    pro = msg.from_user.id
    print(db.find())
    userid = await LeosBot.ask(pro, f"Enter your userid :)")

    loginid = await LeosBot.ask(pro,f"Enter your LOGIN ID ")
    wow = db.find_one({"userid": userid.text, 'loginpass': loginid.text})
    print(wow)
    if wow:
        await bot.send_message(pro,f"Login sucessfully :)")
        print("Hello world")
        y = "yes"
        check = db.find_one({"userid": userid.text, 'loginpass': loginid.text,'refill' : y})
        if check:
            await bot.send_message(pro,f"Already Refilled !!!!")
        else:
            confirm = ["yes","y"]
            refill = await LeosBot.ask(pro,f"Do you wanna refill yes/no ??")
            refill = refill.text.lower()
            if refill in confirm:
                randval = random.randint(100,999)
                refillid = f"refil#{randval}"
                db.update_one({"userid": userid.text, 'loginpass': loginid.text},
                              {"$set": {'refill' : refill,'refillid': refillid}}
                              )
                await bot.send_message(pro,f"Sussessfully registerd refill id {refillid}")
            else:
                await bot.send_message(pro,f"Booking Cancelled :)")
    else:
        await bot.send_message(pro,f"Login failed Oooopzzz unable to authenticate")
        print("owk bieee....")


@LeosBot.on_message(filters.regex("Admin!!"))
async def adminlogin(bot,msg):
    admin = msg.from_user.id
    pwass = Setup.Admin_Pass # ADMIN Pass!
    await bot.send_message(admin,f"its Admin Panel.... kids stay away")
    passd = await LeosBot.ask(admin,f"Admin Password plase >>>>")
    if passd.text == pwass:
        await bot.send_message(admin,f"Sucesss brohh :)")
        viewd = await LeosBot.ask(admin,"View all details>>> press y ")
        total = db.count_documents({})
        fulldb = db.find({})
        print(fulldb)
        await bot.send_message(admin,f"total datas : {total}")
        if viewd.text.lower() == "y":
            y = "yes"
            check = db.find({'refill': y})
            # if check:
            for doc in fulldb:
                if 'refill' in doc:
                    print("myr")
                    FetchedDetails = f"""
Gas booked details
Mongo_id : {doc["_id"]}
User name : {doc["name"]}
Ration Card :{doc["rationCard"]}
Address : {doc["address"]}

Phone no : {doc["phone"]}
user id : {doc["userid"]}
loginPass : {doc["loginpass"]}
refill : {doc["refill"]}
refill id : {doc["refillid"]}
                    """
                    await bot.send_message(admin, FetchedDetails)
                    print(check)
                else:
                    print("hiiii")
                    FetchedDetails = f"""
#New user details
Mongo_id : `{doc["_id"]}`
User name : {doc["name"]}
Ration Card :{doc["rationCard"]}
Address : {doc["address"]}
    
Phone no : {doc["phone"]}
user id : {doc["userid"]}
loginPass : {doc["loginpass"]}
refill : not Booked
                    """
                    await bot.send_message(admin, FetchedDetails)
                    print(check)
                # else:
                #     if :
                #         FetchedDetails = f"""
                #                     Mongo_id : {doc["_id"]}
                #                     User name : {doc["name"]}
                #                     Ration Card :{doc["rationCard"]}
                #                     Address : {doc["address"]}
                #
                #                     Phone no : {doc["phone"]}
                #                     user id : {doc["userid"]}
                #                     loginPass : {doc["loginpass"]}
                #                     refill : Not Booked
                #                     """
                #         await bot.send_message(admin, FetchedDetails)
                #         print(check)
                # else:
                #     for doc in fulldb
                    #     FetchedDetails = f"""
                    #     Mongo_id : {doc["_id"]}
                    #     User name : {doc["name"]}
                    #     Ration Card :{doc["rationCard"]}
                    #     Address : {doc["address"]}
                    #     Phone no : {doc["phone"]}
                    #     user id : {doc["userid"]}
                    #     loginPass : {doc["loginpass"]}
                    #     refill : NULL
                    #     """
                    #     await bot.send_message(admin,FetchedDetails)
                    #     print(check)
        else:
            await bot.send_message(admin,f"OOpx invalid command :) plzz relogin")
    else:
        await bot.send_message(admin,f"leave now...!!!")

LeosBot.run()