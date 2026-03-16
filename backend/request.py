import requests

url = "http://127.0.0.1:1488/auth/telegram"

data = {
    "init_data": "query_id=AAHdF6IQAAAAAN0XohB7g3Pj&user=%7B%22id%22%3A712345678%2C%22first_name%22%3A%22Ivan%22%2C%22username%22%3A%22ivan_dev%22%7D&auth_date=2000000000&hash=1d3d5f7f2d0a3a7b3c4c7a1f9c2c54e3bdbfd83a5c94b9c2d4b5e8a1c7d8e9f0"
}

r = requests.post(url, json=data)

print(r.text)