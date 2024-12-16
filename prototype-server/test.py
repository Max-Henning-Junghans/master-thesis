import http.client
import json
import time

conn = http.client.HTTPConnection("37.27.195.86", 5000)

time_now = time.time()
for x in range(1000):
    payload = json.dumps({
        "s_weather": [
            [
                1726772849 + x,
                20.2 + (x / 100)
            ]
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/measurements", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
print(time.time() - time_now)
