import requests
from django.contrib.auth.models import User
User.objects.create_user(username="ug2319354@ines.ac.rw", password="test1234")


url = "http://127.0.0.1:8000/api/login/"
email = "ug2319354@ines.ac.rw"  # <-- Replace this with actual username
password = "test1234"       # <-- Replace this with actual password

try:
    response = requests.post(url, json={"username": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Login successful!")
        print("Token:", data['token'])
        print("User ID:", data['user_id'])
        print("Username:", data['username'])
    else:
        print("\n❌ Login failed:", response.json())
except requests.exceptions.ConnectionError:
    print("\n❌ Connection error: Unable to reach the server at 127.0.0.1:8000.")
    print("➡️  Make sure your Django server is running with `python manage.py runserver`")
