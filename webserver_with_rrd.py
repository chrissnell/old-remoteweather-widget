#Copyright Jon Berg , turtlemeat.com

import string,cgi,redis,rrdtool

import subprocess
import base64
import simplejson

from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

otemp = ''

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global otemp
        try:
            if self.path.endswith("wx"):
                r = redis.Redis(host='localhost', port=6379, db=0)
                wdir = r.get('wdir')
                wspeed = r.get('wspeed')
                itemp = r.get('itemp')
                otemp = r.get('otemp')
                ihumidity = r.get('ihumidity')
                ohumidity = r.get('ohumidity')
                rainfall = r.get('rainfall')
                pressure = r.get('pressure')
                lastobs = r.get('lastobs')
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write("oh=" + ohumidity + "\n")
                self.wfile.write("ih=" + ihumidity + "\n")
                self.wfile.write("rf=" + rainfall + "\n")
                self.wfile.write("bp=" + pressure + "\n")
                self.wfile.write("wd=" + wdir + "\n")
                self.wfile.write("ws=" + wspeed+ "\n")
                self.wfile.write("ti=" + itemp + "\n")
                self.wfile.write("to=" + otemp + "\n")
                self.wfile.write("lo=" + lastobs + "\n")
                return

            if self.path.startswith("/rrd1w"):
                self.send_response(200)
                self.send_header('Content-type',        'image/png')
                self.end_headers()
                ret = rrdtool.graph("broadmoor_outside.png",
                  "--start", "-10d", "--vertical-label=Degrees",
                  "-w 700", "-h 300",
                  "--title=Broadmoor Bluffs House: Temperature",
                  "DEF:otemp=broadmoor.rrd:otemp:AVERAGE",
                  "DEF:itemp=broadmoor.rrd:itemp:AVERAGE",
                  "AREA:itemp#abd4e0",
                  "AREA:otemp#91BE91",
                  "LINE1:otemp#215E21:Outside Temperature\\r",
                  "LINE1:itemp#8caeb6:Inside Temperature\\r",
                  "COMMENT:\\n",
                  "GPRINT:otemp:LAST:Current\: %.2lf \\r",
                  "GPRINT:otemp:MAX:High\: %.2lf \\r",
                  "GPRINT:otemp:MIN:Low\: %.2lf \\r")
                f = open("/nfs/weather/broadmoor_outside.png")
                self.wfile.write(f.read())
                f.close()
                track("1-week-graph", otemp, 
                             {"method": "webserver", "current-temp": otemp})
                return

            if self.path.startswith("/rrd1d"):
                self.send_response(200)
                self.send_header('Content-type',        'image/png')
                self.end_headers()
                ret = rrdtool.graph("broadmoor_outside_1d.png",
                  "--start", "-1d", "--vertical-label=Degrees",
                  "-w 700", "-h 300",
                  "--title=Broadmoor Bluffs House: Temperature",
                  "DEF:otemp=broadmoor.rrd:otemp:AVERAGE",
                  "DEF:itemp=broadmoor.rrd:itemp:AVERAGE",
                  "AREA:itemp#abd4e0",
                  "AREA:otemp#91BE91",
                  "LINE1:otemp#215E21:Outside Temperature\\r",
                  "LINE1:itemp#8caeb6:Inside Temperature\\r",
                  "COMMENT:\\n",
                  "GPRINT:otemp:LAST:Current\: %.2lf \\r",
                  "GPRINT:otemp:MAX:High\: %.2lf \\r",
                  "GPRINT:otemp:MIN:Low\: %.2lf \\r")
                f = open("/nfs/weather/broadmoor_outside_1d.png")
                self.wfile.write(f.read())
                f.close()
                track("1-day-graph", otemp, 
                             {"method": "webserver", "current-temp": otemp})
                return

            if self.path.startswith("/rrd6h"):
                self.send_response(200)
                self.send_header('Content-type',        'image/png')
                self.end_headers()
                ret = rrdtool.graph("broadmoor_outside_6h.png",
                  "--start", "-6h", "--vertical-label=Degrees",
                  "-w 400", "-h 300",
                  "--title=Broadmoor Bluffs House: Temperature",
                  "DEF:otemp=broadmoor.rrd:otemp:AVERAGE",
                  "DEF:itemp=broadmoor.rrd:itemp:AVERAGE",
                  "AREA:itemp#abd4e0",
                  "AREA:otemp#91BE91",
                  "LINE1:otemp#215E21:Outside Temperature\\r",
                  "LINE1:itemp#8caeb6:Inside Temperature\\r",
                  "COMMENT:\\n",
                  "GPRINT:otemp:LAST:Current\: %.2lf \\r",
                  "GPRINT:otemp:MAX:High\: %.2lf \\r",
                  "GPRINT:otemp:MIN:Low\: %.2lf \\r")
                f = open("/nfs/weather/broadmoor_outside_6h.png")
                self.wfile.write(f.read())
                f.close()
                track("6-hour-graph", otemp, 
                             {"method": "webserver", "current-temp": otemp})
                return


            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def track(event, otemp,  properties=None) :
    if properties == None:
        properties = {}

    token = "0b61550d90e9ff82d2cc7d36e8fd190b"

    if "token" not in properties:
        properties["token"] = token

    params = {"event": event, "properties": properties}
    data = base64.b64encode(simplejson.dumps(params))
    request = "http://api.mixpanel.com/track/?data=" + data
    return subprocess.Popen(("curl",request), stderr=subprocess.PIPE,
        stdout=subprocess.PIPE)

     
def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

