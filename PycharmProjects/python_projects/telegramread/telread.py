from telethon import TelegramClient, events

api_id = 7210281
api_hash = '3b3672b01c29f09313be9f50b9c75926'
client = TelegramClient('anon', api_id, api_hash)
# Notice group of CSE 12 - JUST


@client.on(events.NewMessage(chats='Notice group of CSE 12 - JUST'))
async def my_event_handler(event):
    search = 'docs.google.com'
    print(event.raw_text)
    if search in event.raw_text:
        with open("url_out.txt", "w") as out0:
            out0.write(event.raw_text)
            out0.close()

        file00 = open("url_out.txt", 'r')
        count00 = 0
        st = 'docs.google.com'

        for line in file00:
            count00 += 1
            lines = line.strip()
            if st in lines:
                with open("url_out.txt", "w") as out01:
                    out01.write(lines)
                    out01.close()

        file00.close()

        print(event.raw_text)


client.start()
client.run_until_disconnected()
