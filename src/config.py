import requests

info = {
    "ResponsePort": 8080,
    "Endpoint": requests.get('http://ip.42.pl/raw').text + ":" + str(8080) + "/lambda-response",
    "PublishTopic": "api/iot/pub/"
}
