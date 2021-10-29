# Copyright (C) 2021 twosixtwo projects

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

from flask import Flask
from datetime import datetime
import requests
import platform
import subprocess
import json
from time import sleep
from threading import Thread

config = json.loads(open("config.json", "r").read())

class status_handler:
    def __init__(self):
        self.html = ""
        self.last_timestamp = datetime.now().timestamp()
        self.last = ""
        
    def update_html(self, ping):
        with open("index.html", "r") as _index:
            index = _index.read()
            content = ""
            for x,y in ping.items():
                content += '<p class="text">{}: {}</p>'.format(x,y)
        
            self.html = index.replace("!!!TIMESTAMP!!!", datetime.utcfromtimestamp(status.last_timestamp).strftime('%d.%m.%Y %H:%M:%S') + " UTC")
            self.html = self.html.replace("!!!CONTENT!!!", content)
            self.html = self.html.replace("!!!TITLE!!!", config["title"])
    
    def routine(self):
        output = {}
        for server in config["services"]:
            if server["method"] == "ping":
                response = self.ping(server["ip"])
            elif server["method"] == "http":
                response = self.http(server["ip"])
            else:
                print("ERROR: Unknown method for " + server["name"])
                output[server["name"]] = "configuration error"
                continue

            if response:
                output[server["name"]] = "online"
            else:
                output[server["name"]] = "offline"
        self.last_timestamp = datetime.now().timestamp()
        self.update_html(output)
        self.last = output
        sleep(int(config["time"]))
        self.routine()

    def ping(self, host):
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
    
    def http(self, host):
        request = requests.get(host)
        if request.status_code != 200:
            return False
        else:
            return True

app = Flask(__name__)
status = status_handler()
thread = Thread(target=status.routine)
thread.start()

@app.route("/")
def index():
    status.update_html(status.last)
    return status.html

if __name__ == "__main__":
    app.run()