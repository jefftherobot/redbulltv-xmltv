import sys, urllib.request, xmltv, xml.etree.ElementTree as ET
from datetime import datetime, date, time, timedelta

BASE_URL = "https://appletv-v2.redbull.tv/views/tv"
request = urllib.request.Request(BASE_URL, headers={"Accept" : "application/xml"})
response = urllib.request.urlopen(request)
xml = ET.parse(response)
items = xml.findall('.//twoLineMenuItem')

for element in items:
    label = ''
    if element.find('.//label') is not None:
        label = element.find('.//label').text
    label2 = ''
    if element.find('.//label2') is not None:
        label2 = element.find('.//label2').text
    start = ''
    if element.find('.//rightLabel') is not None:
        start = element.find('.//rightLabel').text
        if start is not None:
            start = datetime.utcfromtimestamp(float(start)).strftime('%Y%m%d%H%M%S%z')
    summary = ''
    if element.find('.//summary') is not None:
        summary = element.find('.//summary').text
    print(label + ' - ' + label2)
    print(start)