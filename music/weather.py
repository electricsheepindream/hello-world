from urllib import request, parse
import json
msg = '淄博'
msg = parse.quote(str(msg))
doc = request.urlopen(url='http://www.sojson.com/open/api/weather/json.shtml?city={city}'.format(city=msg)).read()
res = doc.decode('utf-8')
data = json.loads(res)
con = ''
for i in range(5):
    weather = data['data']['forecast'][i]
    out = '{data}:日出时间:{sunrise},{high},{low},日落：{sunset},天气状况：{tianqi}建议:{notice}\n'.format\
        (data=weather['date'], sunrise=weather['sunrise'], high=weather['high'], low=weather['low'], sunset=weather['sunset'],\
         tianqi=weather['type'], notice=weather['notice'])
    con += out



