# BEN-ASS-NSS-project

# RUN API
python app.py

# RUN Docker Container
- docker network create mynetwork
- docker image build -t assnssproj .
- docker run -p 5001:5000 -d assnssproj --network mynetwork --name ASS-NSS-BEN --device=/dev/ttyUSB0
