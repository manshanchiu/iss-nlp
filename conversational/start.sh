export HOST="127.0.0.1"
export PORT="8081" 


printf "const config = {\"host\":\"$HOST\",\"port\":\"$PORT\"}" > web/config.js

open web/index.html

python server/server.py