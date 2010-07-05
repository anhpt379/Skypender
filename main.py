#! coding: utf-8
## Send message through Skype with multi-thread
#  version: 0.9.1
#  author:  AloneRoad
#  
# see settings.py and default_settings.py to adjust paramenters

from settings import number_of_thread, username, password, users
from workerpool import Job, WorkerPool
from Skype4Py import Skype

print "Connecting..."
api = Skype() # create a Skype API instance 
api.Attach() # connect to Skype
print "Success!"

class Send(Job):
  def __init__(self, user, message):
    self.user = user
    self.message = message
    
  def run(self):
    api.CreateChatWith(self.user).SendMessage(self.message)  
    
if __name__ == "__main__":
  pool = WorkerPool(size=number_of_thread)  # create new pool
  message = "test message"
  users = list(set(open(users).read().split("\n")))
  
  for user in users:
    job = Send(user, message)
    pool.put(job)
  pool.shutdown() # close pool
  pool.wait() # wait to finish