import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/places/%7BplaceId%7D/distance"

querystring = {"toPlaceId":"Q60"}

headers = {
	"x-rapidapi-key": "9c522f288fmshc56d3e61a4bf478p16c2dejsne35fae83a933",
	"x-rapidapi-host": "wft-geo-db.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())



import http.client

conn = http.client.HTTPSConnection("movie-database-alternative.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9c522f288fmshc56d3e61a4bf478p16c2dejsne35fae83a933",
    'x-rapidapi-host': "movie-database-alternative.p.rapidapi.com"
}

conn.request("GET", "/?s=Avengers%20Endgame&r=json&page=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))