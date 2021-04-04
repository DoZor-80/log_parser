# log_parser
This is a simple app for parsing logs

#### 1. Create virtual environment
#### 2. Install dependencies

`python -m pip install -r requirements.txt`

#### 4. Change configuration

`set FLASK_APP=parsix_app.app`

#### 5. Run the app

`python -m flask run --port=8080`

#### 6. Send a file to the server

`curl -F "file=@parsix_app\logs\test.log" http://localhost:8080`
