import cherrypy
import json
from datetime import datetime
import pytz

cherrypy.config.update({'server.socket_port': 5000})

class DailyPanchanga(object):
    @cherrypy.expose
    def index(self, **params):

        if params and params['date']:
            data_key = params['date']
        else:
            tz = pytz.timezone('America/Los_Angeles')
            seattle_now = datetime.now(tz)

            data_key = seattle_now.strftime('%Y-%m-%d')

        json_data = json.load(open('seattle_2019.json'))
        return json.dumps(json_data[data_key], indent=4, ensure_ascii=False)

cherrypy.quickstart(DailyPanchanga(), '/', {'global': {'server.socket_host':'0.0.0.0','server.socket_port': 5000}})
