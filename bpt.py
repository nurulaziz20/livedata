import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from the BotFather
bot_token = '6421868895:AAFMSSvMQKrzZ-2p3C8jFuH5HPPNxbz-UE4'
api_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

# Make a request to the Telegram Bot API to get updates (messages)
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    if 'result' in data:
        results = data['result']
        if results:
            chat_id = results[0]['message']['chat']['id']
            print(f"Chat ID of your bot: {chat_id}")
        else:
            print("No messages received yet. Please send a message to your bot.")
    else:
        print("No 'result' key found in the response data.")
else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
