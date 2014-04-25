#!/usr/bin/env python

import signal
import sys
from subprocess import PIPE, Popen
from threading  import Thread

try: 
   from Queue import Queue, Empty
except ImportError:
   from queue import Queue, Empty  # python 3.x
   
ON_POSIX = 'posix' in sys.builtin_module_names

in_pipe = '/tmp/tele_in'
out_pipe = '/tmp/tele_out'
send_pipe = '/tmp/tele_send'



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
	process.terminate()
        sys.exit(0)


def enqueue_output(output, queue):
    for line in iter(output.readline, b''):
        queue.put(line)

def out_parser(buffer):
    while True:
	try:  line = buffer.get(True) # or q.get(timeout=.1)
	except Empty:
	    print('no output yet')
	else: # got line
	    print line
	    if "BREAK" in line: 
		say()
		print "Break received"
		break

def say():
    f = open('/tmp/tele_send','a')
    tr = Process (target=process.communicate,args=("msg Servers OK",))
    tr.daemon = True
    tr.start()
    #f.write(msg)
    #f.write()
    #f.close()
    #process.communicate("msg Servers OK\n")

   
process = Popen(['/usr/sbin/telegram'], stdout=PIPE, stdin=PIPE, bufsize=1, close_fds=ON_POSIX)
out_buffer = Queue()
t = Thread(target=enqueue_output, args=(process.stdout, out_buffer))
t1 = Thread(target=out_parser, args=(out_buffer,))
t.daemon = True 
t1.daemon = True
print "starting queue thread"
t.start()

#process.communicate("status")

t1.start()
t1.join()
# ... do other things here
