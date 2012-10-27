#! /usr/bin/python
import sys, os, string, json, urllib3, time
if len(sys.argv) < 4:
   print("""
getCrunchbase -- downloads jsons for crunchbase list
usage:
   getCrunchbase [ENTRY TYPE] [JSON-LIST] [TARGET DIRECTORY] (LAST SUCCESSFUL)""")
   sys.exit(0)

cbtype = sys.argv[1]

lastSuccess = 0
if len (sys.argv) > 4:
   lastSuccess = sys.argv[4]

with open (sys.argv[2], 'r') as infile:
   data = json.load(infile)
   if not os.path.exists(sys.argv[3]):
      os.makedirs(sys.argv[3])
   http = urllib3.PoolManager()

   if lastSuccess:
      print ("lastSuccess present as " + str(lastSuccess))
      while (True):   
         entry = data.pop(0)
         if entry['permalink'] == str(lastSuccess):
            break

   errfile_name = "ERRS"
   errfile_dir = sys.argv[3]
   if errfile_dir[-1] == '/':
      errfile_path = errfile_dir + errfile_name
   else:
      errfile_path = errfile_dir + "/" + errfile_name
   
   with open(errfile_path, 'w+') as errfile:

      for entry in data:
         print(entry)
         link = entry['permalink']
         filename = sys.argv[3] + link
         noContinue = True
         failures = 0
         fail_limit = 5
         #only download if no existing file
         if not os.path.exists(filename):
            while (noContinue):
               url = 'http://api.crunchbase.com/v/1/' + cbtype + '/' + link + '.js?api_key=56768vu8jak9atqqb5ugr5uc'
               resp = http.request('GET', url)
               if resp.status >= 400 and resp.status < 500:
                  print("""oh shit error status """ + str(resp.status) + " for " + url + ". retrying...")
                  errfile.write(link + " returned " + str(resp.status))
                  failures += 1
                  if failures > fail_limit:
                     noContinue = False 
               elif resp.status == 200:
                  with open(filename, 'w+') as outfile:
                     outfile.write(resp.data.decode("utf-8"))
                  noContinue = False
               else:
                  print("error status " + str(resp.status) + ". retrying...")
                  failures += 1
                  if failures > fail_limit:
                     noContinue = False 

