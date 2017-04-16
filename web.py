OUTPUT_FILE = '/var/www/html/web/subscribedlist'

import os.path

def action(query):

   if query not in open(OUTPUT_FILE).read():
      file = open(OUTPUT_FILE,'a')
      file.write('"' + query + '"' + '\n')
      print("IP was not in list")
   else:
      print("IP is already in list")
