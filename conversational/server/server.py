import asyncio
import websockets
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


batchesRequest = {}

async def handle_image(websocket, path):
    print("WebSocket connection established")
    async for message in websocket:
        # Decode image data
        try:
            # message should include gsheet link and image
            data = json.loads(message)
            link = data["link"]
            image_data = data["image"]
            id = data["id"]
            proceed = data["proceed"]
            if id not in batchesRequest:
                batchesRequest[id] = {
                    "link":link,
                    "image": image_data,
                    "id": id
                }
            else:
                batchesRequest[id]["image"] += image_data
            if proceed:
                result = process(batchesRequest[id])
                del batchesRequest[id]
                await websocket.send(json.dumps(result))
        except Exception as e:
            await websocket.send(json.dumps({
                "ocr_result": [],
                "found_row": {}
            }))
                    
        

    print("WebSocket connection closed")

def process(data):
    link = data["link"]
    image_data = data["image"]
    inventory = load_inventroy_data(link)
    image_data = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_data))   
    result = ocr.ocr(np.array(image))
    print(result)
    txts = [line[1][0] for line in result[0]]
    print(txts)
    found_row = findRow(inventory,txts)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    # Send OCR result back to client
    return {
        "ocr_result": result,
        "found_row": found_row
    }

    
def findRow(inventory,ocr_result: list):
    # assume ocr_result is a list of text
    header = inventory[0]
    foundItem = []
    for item in inventory[1:]:
        # itme[0] is the P/N
        for res in ocr_result:
            if item[0] in res:
                foundItem = item
                break
        else:
            continue
        break
    d = {}
    if len(foundItem) > 0:
        # build dict
        for idx,v in enumerate(header):
            d[v] = foundItem[idx]
    return d
    


# Start WebSocket server
async def start_server():
    async with websockets.serve(handle_image, os.environ['HOST'], os.environ['PORT']):
        await asyncio.Future()

asyncio.run(start_server())
