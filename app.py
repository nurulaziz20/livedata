from flask import Flask, render_template
import requests
import schedule
import time

app = Flask(__name__)

# Function to fetch data from the API
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

def convert_to_cm(tinggi_air_mm):
  return int(tinggi_air_mm) / 10



#fetched data
def process_data():
    data_list = fetch_data()
    for data in data_list:
        data['TINGGI_AIR'] = convert_to_cm(data['TINGGI_AIR'])
        data['TINGGI_AIR'] = str(data['TINGGI_AIR']).rstrip(".0")
    return data_list



# Schedule tiap 5 minutes
schedule.every(5).minutes.do(process_data)


def main():
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    
    app.run(debug=True)

# Flask route to render the data on a webpage
@app.route('/')
def home():
    return render_template('home.html')

# Flask route to render the "Data" page
@app.route('/data')
def show_data():
    data_list = process_data()
    return render_template('data.html', data_list=data_list)


if __name__ == "__main__":
    main()
