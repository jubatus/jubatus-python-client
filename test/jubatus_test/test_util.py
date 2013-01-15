import os, sys
import time
import signal
from threading import Timer

import msgpackrpc
from msgpackrpc.error import *

class TestUtil:
  @staticmethod
  def wait_server(port):
    sleep_time = 1000 # usec
    # 1000 * \sum {i=0..9} 2^i = 1024000 micro sec = 1024 ms
    for i in range(10):
        # For Python clients, we need to generate instance for each iteration.
        cli = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port))
        time.sleep(sleep_time/1000000.0) # from usec to sec
        try:
            cli.call("dummy")
            raise Exception("dummy rpc succeeded")
        except RPCError, e:
            if e.args[0] == 1: # "no such method"
                return         # ... means server is fully up
        sleep_time *= 2;
    raise Exception("cannot connect")

  @staticmethod
  def fork_process(name, port = 9199, config = ""):
    cmd = "juba" + name

    try:
      child = os.fork()
      if child == 0:
        os.execvp(cmd, [cmd, "--rpc-port", str(port), "--configpath", config, "--thread", "100", "--datadir", "."])
      elif child < 0:
        print 'fork error'
        sys.exit(1)
      TestUtil.wait_server(port)
      return child
    except OSError as error:
      print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
      sys.exit(1)

  @staticmethod
  def kill_process(child):
    if os.kill(child, signal.SIGTERM) is not None:
      print 'kill error'
    t = Timer(3.0, os.kill, [child, signal.SIGKILL])
    t.start()
    os.waitpid(child, 0)
    t.cancel()

  @staticmethod
  def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()
