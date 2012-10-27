#! /usr/bin/python

import notify2, sys, subprocess, re, time

lastnum = 0
while (True):
      proc = subprocess.Popen(["du", "-sh", "/home/bistenes/TechRank/"], stdout=subprocess.PIPE)
      out, err = proc.communicate()
      num = int (re.sub (r"\D", "", out.decode('utf-8')))
      if num > lastnum + 50:
         lastnum = num
         if notify2.init("crawl monitor"):
            alert = notify2.Notification("Another 50M Downloaded", out.decode('utf-8'))
            alert.show()
         else:
            print("pynofity error")
      time.sleep(10)
