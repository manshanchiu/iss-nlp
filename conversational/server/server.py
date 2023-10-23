import asyncio
import websockets
import json
import os
import gsheet
import openai
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

gsheet_data_dict = list[dict]
countries = list[str]
gsheet_datadf = pd.DataFrame()
paramFormat = {
    "country": "country code"
}
sentimentMapping = {
    "1": "Very Unhappy",
    "2": "Unhappy",
    "3": "Neutral",
    "4": "Happy",
    "5": "Very Happy"
}

def number_of_reviews_from_country(params:dict):
    count = 0
    for row in gsheet_data_dict:
        if row["country"] == params["country"]:
            count += 1
    return count

def total_reviews(params:dict):
    return len(gsheet_data_dict)

def get_issue_types(params:dict):
    return gsheet_datadf["issues"].unique().tolist()

def get_number_of_issue_types(params:dict):
    return len(gsheet_datadf["issues"].unique().tolist())

def get_issue_types_from_country(params:dict):
    return gsheet_datadf[gsheet_datadf["country"] == params["country"]]["issues"].unique().tolist()
def get_number_of_issue_types_from_country(params:dict):
    return len(gsheet_datadf[gsheet_datadf["country"] == params["country"]]["issues"].unique().tolist())

def get_sentiment_distribution_with_percentage(params:dict):
    sentiment = gsheet_datadf["sentiment"].value_counts(normalize=True)
    sentimentAcutal = gsheet_datadf["sentiment"].value_counts()
    # format it to actual number (percentage)
    sentiment = sentiment * 100
    # round to 2 decimal places
    sentiment = sentiment.round(2)
    out = ""
    for key in sentiment.keys():
        out += f"{key}: {sentimentAcutal[key]} ({sentiment[key]}%), "
    return out

def get_country_sentiment_distribution_with_percentage(params:dict):
    sentiment = gsheet_datadf[gsheet_datadf["country"] == params["country"]]["sentiment"].value_counts(normalize=True)
    sentimentAcutal = gsheet_datadf[gsheet_datadf["country"] == params["country"]]["sentiment"].value_counts()
    # format it to actual number (percentage)
    sentiment = sentiment * 100
    # round to 2 decimal places
    sentiment = sentiment.round(2)
    out = ""
    for key in sentiment.keys():
        out += f"{key}: {sentimentAcutal[key]} ({sentiment[key]}%), "
    return out

async def handle_message(websocket, path):
    print("WebSocket connection established")
    async for message in websocket:
        # Decode image data
        try:
            # message should include gsheet link and image
            data = json.loads(message)
            question= data["message"]
            print(question)
            r = askGPT(question)
            # try to parse to json
            try:
                data = json.loads(r)
                print(data)
                func = globals()[data["func"]]
                if "params" in data:
                    d = func(data["params"])
                    userres = gptResponse(question,d)
                else:
                    userres = func({})
                result = {
                    "message": userres
                }
                    
            except Exception as e:
                # if error, just response the message
                print(e)
                print("Failed to parse answer")
                result = {
                    "message": r
                }
            print("event after error")
            await websocket.send(json.dumps(result))
        except Exception as e:
            print(e)
            await websocket.send(json.dumps({
                "ocr_result": [],
                "found_row": {}
            }))
                    
        

    print("WebSocket connection closed")

def askGPT(question):
    response = openai.ChatCompletion.create(
        engine="gpt-4-32k",
        model="gpt-3.5-turbo",
        max_tokens = 2000,
        temperature=0, 
        messages=[
            {"role": "system", "content": 
                    f"""You are a helpful assistant. I have a list of reviews from a website. 
                    I will perform the relevant action based in the user's ask. You job is to help me to classify my question into few categories (summary/price/quality) and i will call the relevant function to get the result.
                    If you are not sure, just try to ask the user question to get more information.
                    If you are sure, return me the function name in json format key1: "func", value1 is the function name. key2: "params" which value is a json ({json.dumps(paramFormat)}).
                    Here are the list of functions you can call:
                    1. total_reviews -> return total number of reviews
                    2. number_of_reviews_from_country(country) -> return number of reviews from a country
                    3. get_issue_types -> return list of issue types
                    4. get_number_of_issue_types -> return number of issue types
                    5. get_issue_types_from_country -> return list of issue types from a country
                    6. get_number_of_issue_types_from_country -> return number of issue types from a country
                    7. get_sentiment_distribution_with_percentage -> return sentiment distribution
                    8. get_country_sentiment_distribution_with_percentage -> return sentiment distribution from a country
                    Help me convert the contry to the list of country code here as well: {countries}
                    """},
            {"role": "user", "content": question},
        ]
    )
    print(response)
    return response["choices"][0]["message"]["content"]

def gptResponse(question,data):
    response = openai.ChatCompletion.create(
    engine="gpt-4-32k",
    model="gpt-3.5-turbo",
    max_tokens = 2000,
    temperature=0, 
    messages=[
            {"role": "system", "content": 
                    f"""You are a helpful assistant. User asked me a question: {question} and i have gottern the data : {data}
                    Help me to format the response to user
                    """},
        ]
    )
    return response["choices"][0]["message"]["content"]
# Start WebSocket server
async def start_server():
    async with websockets.serve(handle_message, os.environ['HOST'], os.environ['PORT']):
        print("Server started")
        await asyncio.Future()



if __name__ == "__main__":
    # preparing data
    gsheet_helper = gsheet.Gheet("https://docs.google.com/spreadsheets/d/1j2YMFEvy6aRPD52o_CaVAKqMZCzubna1_9gXiufsInw")    
    gsheet_data = gsheet_helper.load_sheet()
    gsheet_data_dict = gsheet_helper.to_dict(gsheet_data)
    headers = gsheet_data[0]
    headers = [x.lower() for x in headers]
    gsheet_data = gsheet_data[1:]
    df = pd.DataFrame(gsheet_data,columns=headers)
    df = df.dropna()
    # replace sentiment with the right mapping
    df["sentiment"] = df["sentiment"].apply(lambda x: sentimentMapping[x])
    gsheet_datadf = df
    # get unique values of header "Country"
    countries = df["country"].unique().tolist()
    asyncio.run(start_server())