# This program is to develop the APIs to get the schedule. 
# This is useful for any app-developer to integrate the ScheduleBuddy to any page/app
# User can also automate functionality using the ScheduleBuddy API
import uvicorn
import pymongo
from  fastapi import FastAPI
from model import QueryDates
import pandas as pd
import json
from decouple import config
app = FastAPI(title = " ScheduleBuddy API Docs", version = "1.0.0", debug = True)
mongo_string = config('mongo_string',default='')

# router for index page
@app.get("/")
def index ():
    return {"message" : " Welcome to ScheduleBuddy API Docs Page"}

# API to get the the schedules
@app.post("/get-schedules")
def get_schedule (*, querydates : QueryDates):
    fromtime = querydates.fromtime
    totime = querydates.totime
    # get the data from mongo db
    client = pymongo.MongoClient(mongo_string)
    db = client.ScheduleBuddy
    tasks = db.Tasks.find()
    # store it into the pandas dataframe  
    df = pd.DataFrame(columns=['Time','Title'])
    for task in tasks:
        df = df.append(pd.DataFrame({"Time":[task['Time']],"Title":[task['Title']]}))
    # filter the dataframe based on fromtime and totime in the request body
    df['Time'] = pd.to_datetime(df['Time'])
    mask = (df['Time'] > fromtime) & (df['Time'] <= totime)
    df = df.loc[mask]
    # generate json from the dataframe and return it to the response body
    df = df.to_json(orient='records', date_format='iso')
    return json.loads(df)

if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0", port = 6000)