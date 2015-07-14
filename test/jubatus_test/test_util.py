import os, sys
import time
import signal
from threading import Timer
import subprocess

import msgpackrpc
from msgpackrpc.error import *

import logging

logging.getLogger().setLevel(logging.ERROR)

class TestUtil:
    @staticmethod
    def check_server(port):
        # For Python clients, we need to generate instance for each iteration.
        cli = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", port))
        try:
            cli.call("dummy")
            raise Exception("dummy rpc succeeded")
        except RPCError as e:
            if e.args[0] == 1: # "no such method"
                cli.close()
                return True                 # ... means server is fully up
        cli.close()
        return False

    @staticmethod
    def wait_server(port, proc):
        sleep_time = 1000 # usec
        # 1000 * \sum {i=0..9} 2^i = 1024000 micro sec = 1024 ms
        for i in range(10):
                time.sleep(sleep_time/1000000.0) # from usec to sec
                if TestUtil.check_server(port):
                    return
                if proc.poll():
                    stderr = proc.stderr.read()
                    raise Exception('Cannot run server process: \n{0}'.format(stderr))
                sleep_time *= 2;
        raise Exception("cannot connect")

    @staticmethod
    def fork_process(name, port = 9199, config = ""):
        cmd = "juba" + name
        args = [cmd, "--rpc-port", str(port), "--configpath", config, "--thread", "100", "--datadir", "."]
        try:
            if TestUtil.check_server(port):
                raise Exception('Another server is already running')
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            # use PIPE to suppress log messages of server processes
            try:
                TestUtil.wait_server(port, proc)
            except Exception:
                proc.kill()
                raise
            if proc.poll():
                stderr = proc.stderr.read()
                raise Exception('Cannot run server process: \n' + stderr)
            return proc
        except OSError as error:
            print('Unable to fork. Error: {0} ({1})'.format(error.errno, error.strerror))
            raise error

    @staticmethod
    def kill_process(process):
        process.terminate()
        process.communicate()

    @staticmethod
    def write_file(path, data):
        with open(path, 'w') as f:
            f.write(data)
