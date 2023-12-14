import requests

url = "https://dsda.jakarta.go.id/api/alattma"

# Get the service information
response = requests.get(url + "?f=json")
service_info = response.json()

if isinstance(service_info, list) and len(service_info) > 0:
    unique_siaga_values = set()

    for item in service_info:
        status_siaga = item.get("STATUS_SIAGA")
        if status_siaga:
            unique_siaga_values.add(status_siaga)

    num_unique_siaga_values = len(unique_siaga_values)
    print("Number of unique STATUS_SIAGA values:", num_unique_siaga_values)

    print("Unique STATUS_SIAGA values:")
    for value in unique_siaga_values:
        print(value)
else:
    print("Invalid or empty response")
