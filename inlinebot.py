import requests
import asyncio
from aiogram import Bot, Dispatcher, types

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token.
TELEGRAM_BOT_TOKEN = '6421868895:AAFMSSvMQKrzZ-2p3C8jFuH5HPPNxbz-UE4'

# Function to fetch data from the API Tinggi Muka Air
def fetch_data():
    url = 'https://dsda.jakarta.go.id/api/alattma'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8,ht;q=0.7',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return []

# Function to process and use the fetched data
def process_data():
    data_list = fetch_data()
    return data_list

# Function to format the data as a string
def format_data(data_list):
    formatted_data = "Tinggi Mata Air berdasarkan Pintu Mata Air\n"
    formatted_data += "=" * 20 + "\n" 
    for item in data_list:
        formatted_data += f"Name: {item['NAMA_PINTU_AIR']}\n"
        formatted_data += f"Location: {item['LOKASI']}\n"
        formatted_data += f"Water Height: {int(item['TINGGI_AIR'])/10} cm\n"  # Convert to integer before dividing by 10
        formatted_data += f"{item['STATUS_SIAGA']}\n"
        formatted_data += f"Tanggal: {item['TANGGAL']}\n"
        formatted_data += "-" * 20 + "\n"  # Add a separator line between entries
    return formatted_data
    

async def pintu_air_command(message: types.Message):
    data_list = process_data()
    formatted_data = format_data(data_list)
    await message.reply(formatted_data)

async def stop_command(message: types.Message):
    await message.reply("Bot stopped.")
    # Here you can add any cleanup or saving operations before stopping the bot.
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.close()

async def main():
    global dp
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)

    # Add the /pintuair command handler
    dp.register_message_handler(pintu_air_command, commands=['tma'])

    # Add the /stopbot command handler
    dp.register_message_handler(stop_command, commands=['stop'])

    # Start the Bot
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
