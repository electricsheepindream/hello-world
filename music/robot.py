from werobot import WeRoBot
from urllib import request, parse
import json
robot = WeRoBot(enable_session=False,
                token='esid',
                APP_ID='wxc6ec8eda771e9cf2',
                APP_SECRET='99e8d052e83864de0df9c973382b5ffd'
                )
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


@robot.text
def hello(message):
    if message == '天气':
        return con



