import requests

url = "https://api.brightdata.com/dca/trigger"
headers = {
	"Authorization": "Bearer ef4b61a2-e888-4e1b-8b39-509977b501c7",
	"Content-Type": "application/json",
}
params = {
	"collector": "c_mt0d6wtd2m2qernptv",
	"queue_next": "1",
}
data = [
	{"url":"https://www.meesho.com/search?q=home%20tools&searchType=autosuggest&searchIdentifier=text_search"},
]

response = requests.post(url, headers=headers, params=params, json=data)
print("Status Code:", response.status_code)
print("Response:", response.text)