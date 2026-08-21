import requests

url = "https://api.brightdata.com/dca/dataset"
headers = {
	"Authorization": "Bearer ef4b61a2-e888-4e1b-8b39-509977b501c7",
}
params = {
	"id": "j_mt0fwmk87ncb8mxl3",
}

response = requests.get(url, headers=headers, params=params)
print("Status Code:", response.status_code)
print("Response:", response.text)