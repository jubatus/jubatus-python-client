import os
import time
import signal

import msgpackrpc
from msgpackrpc.error import *

class CommonUtils:
  @staticmethod
  def start_server(name, port):
    try:
      pid = os.fork()
      if pid < 0:
        print 'fork error'
        sys.exit(1)
      elif pid == 0:
        os.execvp(name, [name, "-p", str(port), "-c", "100"])
      CommonUtils.wait_server(port)
      return pid
    except OSError as error:
      print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
      sys.exit(1)

  @staticmethod
  def stop_server(pid):
    if os.kill(pid, signal.SIGTERM) != None:
      print 'kill error'
    os.waitpid(pid, 0)

  @staticmethod
  def wait_server(port):
    sleep_time = 1000 # usec
    # 1000 * \sum {i=0..9} 2^i = 1024000 micro sec = 1024 ms
    for i in range(10):
	    # For Python clients, we need to generate instance for each iteration.
        cli = msgpackrpc.Client(msgpackrpc.Address("localhost", port))
        time.sleep(sleep_time/1000000.0) # from usec to sec
        try:
        	cli.call("dummy")
        	raise Exception("dummy rpc succeeded")
        except RPCError, e:
            if e.args[0] == 1: # "no such method"
                return         # ... means server is fully up
        sleep_time *= 2;
    raise Exception("cannot connect")
