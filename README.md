# ISS NLP Project

## Folder structure
* [/conversational](./conversational): conversation ui code
* [/tableau_dashboard](./tableau_dashboard) tableau dashboard 
* [/model_training](./model_training) code for all the model training


## Run the Chat interface
### 1. install dependencies
```bash
pip install -r conversational/requirements.txt
```
### 2. create a `.env` file to put your openai secret. Can refer to `.env.sample` for the sample
```bash
OPENAI_API_BASE=https://xxxxx
OPENAI_API_VERSION=2023-06-01-preview
OPENAI_API_KEY=xxxxxx
OPENAI_API_TYPE=azure
```
### 3. Put your google service account under the root directory (It is used to read the google sheet data)
### 4. Start the server
```bash
sh conversational/start.sh #this will start the websocket server and open the webpage
```
Demo
![](https://github.com/manshanchiu/iss-nlp/blob/master/images/chat_interface.png)


## License
[MIT](https://choosealicense.com/licenses/mit/)