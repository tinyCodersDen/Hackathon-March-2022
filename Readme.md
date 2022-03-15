# Hackathon-March-2022

Hello, this is repository for what I made in a hackathon in March 2022. My project is a to-do app, and I called it ScheduleBuddy. Check out the different features and don't forget to explore the project's independant API!
## Instructions for running:
First, you will need to install the required modules:
```shell
pip install -r requirements.txt
```
Second, you need to set up the .env file, make sure you create a blank .env and enter values in the following format:
```make
SENDGRID_API_KEY = '<SENDGRID API_KEY HERE>'
mongo_string = '<MONGODB_KEY HERE>'
sender_email = '<YOUR SENDER_EMAIL HERE>'
```
Replace the values in the string with your keys and paste it into your .env file.

Once you are done with your API Keys setup, run these commands on **2 seperate windows** in your terminal:
```python
python app.py
```
In the other terminal:
```bash
uvicorn myapi:app --reload
```
