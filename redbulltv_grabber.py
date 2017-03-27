import sys, re, urllib.request, xmltv, xml.etree.ElementTree as ET
from datetime import datetime, date, time, timedelta

BASE_URL = "https://appletv-v2.redbull.tv/views/tv"
request = urllib.request.Request(BASE_URL, headers={"Accept" : "application/xml"})
response = urllib.request.urlopen(request)
xml = ET.parse(response)
items = xml.findall('.//twoLineMenuItem')

w = xmltv.Writer()

w.addChannel({'display-name': [(u'Red Bull TV', u'en')],'id': u'hls.redbulltv'})

for i, element in enumerate(items):
    programme = {"channel":'hls.redbulltv', "title":[], "sub-title":[], "desc":[], "start":'', "stop":''}

    label = u''
    if element.find('.//label') is not None:
        label = element.find('.//label').text
    label2 = ''
    if element.find('.//label2') is not None:
        label2 = element.find('.//label2').text
    start = ''
    if element.find('.//rightLabel') is not None:
        start = element.find('.//rightLabel').text
        if start is not None:
            start = datetime.utcfromtimestamp(float(start))
        else:
            start = datetime.utcnow()#.strftime('%Y%m%d%H%M%S%z')

    # Set end has start to calculate duration from
    end = ''

    if i < (len(items) - 1):
        #End this program at the start of the next program
        end = items[i + 1].find('.//rightLabel').text
        if end is not None:
            end = datetime.utcfromtimestamp(float(end))
        else:
            end = datetime.utcnow()
    else:
        #This is the last program, so use duraction to calculate end
        if element.find('.//footnote') is not None:
            end = element.find('.//footnote').text
            if end is not None:
                duration = end.replace('Duration: ', '')
                duration = duration.split(',')
                totalDuration = start
                for i in duration:
                    if 'hour' in i:
                        totalDuration = totalDuration + timedelta(hours=int(re.sub(r' hours?', "",i)))
                    elif 'minute' in i:
                        totalDuration = totalDuration + timedelta(minutes=int(re.sub(r' minutes?', "", i)))
                    elif 'second' in i:
                        totalDuration = totalDuration + timedelta(seconds=int(re.sub(r' seconds?', "", i)))
                end = totalDuration

    summary = ''
    if element.find('.//summary') is not None:
        summary = element.find('.//summary').text

    programme["title"] = [(label, u'')]
    programme["sub-title"] = [(label2, u'')]
    programme["desc"] = [(summary, u'')]
    programme["start"] = start.strftime('%Y%m%d%H%M%S%z')
    programme["stop"] = end.strftime('%Y%m%d%H%M%S%z')

    # print(programme)

    w.addProgramme(programme)

w.write('redbull.xml', pretty_print=True)