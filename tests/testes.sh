API_HOST=10.220.0.15
API_PORT=8080

curl -X POST http://$API_HOST:$API_PORT/core/new -H 'Content-Type: application/json' -d '{"external_pid":"doi-number"}'

ARK_ID_INVALID=8033/fkwff300000000005v6
ARK_ID=8033/fkwff300000000005v7
# 8033/fkwff300000000005w1
# 8033/fkwff300000000005xt

curl -X GET http://$API_HOST:$API_PORT/core/get/$ARK_ID

##
## URL
##
#DEFAULT=NONE

valid_url=http://www.uol.com/123456
invalid_url='ola mundo 12345'


curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"external_url":"$invalid_url"}'
curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"external_url":"$valid_url"}'

##
## EXTERNAL URL
##

#DEFAULT=NONE
INVALID_DOI=DOIXPTO
VALID_DOI=doi:/116.jdakt.7892

# INVALID_DARK
curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID_INVALID -H 'Content-Type: application/json' -d '{"external_pid":"$VALID_DOI"}'

curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"external_pid":"$INVALID_DOI"}'
curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"external_pid":"$VALID_DOI"}'


##
## PAYLOAD
##

invalid_payload='{x:y}'
valid_payload='{'x':'y'}'


curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"payload":"$invalid_payload"}'
curl -X POST http://$API_HOST:$API_PORT/core/set/$ARK_ID -H 'Content-Type: application/json' -d '{"payload":"$valid_payload"}'