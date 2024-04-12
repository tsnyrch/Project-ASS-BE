# BEN-ASS-NSS-project

# RUN API
python app.py

docker image build -t assnssproj .
docker run -p 5001:5000 -d assnssproj