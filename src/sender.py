import requests
import os
import logging as log
from database import Database 

class Sender:
    def __init__(self):
        self.db = Database()
        

    def send_unsent(self):

        # send

        log.debug("init send_unsent")
        # mark as sent where all ok

        unsent = self.db.get_time_entries_where_unsent()

        for u in unsent:
            
            data = {'rfid': u[1], 'time': u[4].strftime("%Y-%m-%d %H:%M:%S")}
            url = os.environ.get("API_URL") + "/timeentries/ringin"
            
            response = requests.post(url, data=data)

            if response.status_code == 200:
                self.db.set_time_entry_sent(id=u[0])
                log.info("successfull timeentry upload: %s" % u[1])
            elif response.status_code == 401:
                log.info("response: 401, Unauthorized")
            elif response.status_code == 403:
                log.info("response: 403, server is refusing action")
            elif response.status_code == 404:
                self.db.set_time_entry_not_exist(id=u[0])
                log.info("response: 404, rfid not in use: %s" % u[1])
            elif response.status_code == 407:
                log.info("response: 407, Proxy Authentication Required")
            elif response.status_code == 408:
                log.info("response: 408, Request Timeout")
            else:
                # somehow the server does not work as intended, ignore
                log.error(response.json)
        
        self.db.close_connection()
