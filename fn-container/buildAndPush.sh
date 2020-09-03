docker build -t rawkintrevo/goatrodeo:latest .
docker push rawkintrevo/goatrodeo:latest

ibmcloud fn action create goatrodeo --docker rawkintrevo/goatrodeo:latest
