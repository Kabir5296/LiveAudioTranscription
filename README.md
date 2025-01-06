# Live Audio Transcription
By Mahfuzul Kabir,
Machine Learning Engineer,
ACI Limited

# USE:
Install Requirements
```
python3.9 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Install Javascript Dependencies
```
sudo npm install http-server
```

Run Static HTML Page as a Client at Port 8080
```
http-server
```

Run Uvicorn as a Server at Port 8000
```
python server.py
```

Access the test client at http://localhost:8080
Make sure to use localhost and http, since ip:port won't work without SSL verification.