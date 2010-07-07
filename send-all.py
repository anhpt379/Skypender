#! coding: utf-8
## Send message through Skype with multi-thread
#  version: 0.9.1
#  author:  AloneRoad
#  
# see settings.py and default_settings.py to adjust paramenters

from settings import pool_size, message
from workerpool import Job, WorkerPool
from Skype4Py import Skype

print "Connecting..."
api = Skype() # create a Skype API instance 
api.Attach() # connect to Skype
current = None
total = None

class Send(Job):
  def __init__(self, user, message):
    self.user = user
    self.message = message
    
  def run(self):
    api.CreateChatWith(self.user).SendMessage(self.message) 
    print "Sending...  %3.2f" % (current * 100 / float(total))
    current += 1 
    
if __name__ == "__main__":
  pool = WorkerPool(size=pool_size)  # create new pool
  message = open(message).read()
   
  print "Sending message..."
  total = api.Friends.Count
  print "Total: %s" % total
  
  current = 0
  
  for user in list(api.Friends):
    job = Send(user.Handle, message)
    pool.put(job)
  
  print "Shutting down..."
  pool.shutdown() # close pool
  pool.wait() # wait to finish
  
  print "Done."