export HOST="127.0.0.1"
export PORT="8081" 


printf "const config = {\"host\":\"$HOST\",\"port\":\"$PORT\"}" > conversationalweb/config.js

open conversational/web/index.html

python3 conversational/server/server.py