import http.client
import json

conn = http.client.HTTPSConnection("movie-database-alternative.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9c522f288fmshc56d3e61a4bf478p16c2dejsne35fae83a933",
    'x-rapidapi-host': "movie-database-alternative.p.rapidapi.com"
}

conn.request("GET", "/?s=Avengers%20Endgame&r=json&page=1", headers=headers)

res = conn.getresponse()
data = res.read()

# Преобразуем ответ в формат JSON
response_json = json.loads(data.decode("utf-8"))

# Печатаем форматированный JSON (или используем данные по назначению)
print(json.dumps(response_json, indent=4))
