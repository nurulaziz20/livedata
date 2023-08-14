import requests
import json

url = "https://dsda.jakarta.go.id/api/curahhujan"

# Get the service information
response = requests.get(url + "?f=json")
service_info = response.json()

if "error" in service_info:
    print("Error:", service_info["error"]["message"])
else:
    # Save the service information to a file
    with open("service_info.json", "w") as json_file:
        json.dump(service_info, json_file, indent=4)

    print("Service information saved to 'service_info.json'")
