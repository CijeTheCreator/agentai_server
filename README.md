# Flask Rest API For FraudWatch, built for the AgentAI DevChallenge

The Implementation for the WhatsApp Chatbot is located at [https://github.com/CijeTheCreator/fraudwatch_chatbot.git](https://github.com/CijeTheCreator/fraudwatch_chatbot.git)
The App Downloads the call recordings into the S3 Details specified below

## Download and install locally

1. `https://github.com/CijeTheCreator/agentai_server`
2. `cd agentai_server`
3. `mkvirtualenv agentai_server`
4. `pip install -r requirements.txt`

## Set local environment variables

```
cd ~/Projects/simple-flask-s3-uploader
export APP_SETTINGS="config.DevelopmentConfig"
export SECRET_KEY="your-random-secret-key"
export S3_BUCKET="your-bucket-name"
export S3_KEY="your-aws-secret-key"
export S3_SECRET_ACCESS_KEY="your-aws-secret-access-key"
```

## Run it!

1. `export FLASK_APP=app.py`
2. `flask run`
