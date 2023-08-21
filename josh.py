import os
cwd = os.getcwd()
with open(f"{os.getenv('userprofile')}\\msg2u.txt", "w") as f:
  f.write("Don't ever trust anybody.")

def sendmsg(msg):
  import _thread
  _thread.start_new_thread(lambda : os.system(msg), ())

for i in range(1):
    sendmsg(f"notepad {os.getenv('userprofile')}\\msg2u.txt")
