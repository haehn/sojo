import signal
import socket
import sys
import tornado
import tornado.gen
import tornado.web
from concurrent.futures import ThreadPoolExecutor # pip install futures

class MainHandler(tornado.web.RequestHandler):
  '''
  Our custom request handler who implements a co-routine
  and forwards the calls to an external class instance (core).
  '''

  def initialize(self, executor, webserver):
    self._executor = executor
    self._webserver = webserver

  @tornado.gen.coroutine
  def get(self, uri):
    '''
    '''

    content, content_type = yield self._executor.submit(self._webserver._manager.get, request=self.request)
    self.set_header('Access-Control-Allow-Origin', '*')
    self.set_header('Content-Type', content_type)
    self.write(content)


class Webserver:

  def __init__(self, manager, port=8000):
    '''
    '''
    self._manager = manager
    self._port = port

  def start(self):
    '''
    '''

    signal.signal(signal.SIGINT, self.close)
    ip = socket.gethostbyname(socket.gethostname())

    # the important part here is the ThreadPoolExecutor being
    # passed to the main handler, as well as an instance of core
    webapp = tornado.web.Application([
        (r'/c/sojo/s/(.*)', tornado.web.StaticFileHandler, {'path': '_web/', 'default_filename': 'index.html'}),
        (r'(/c/)', MainHandler, {'executor':ThreadPoolExecutor(max_workers=10),
                                 'webserver':self}),
    ])
    webapp.listen(self._port)


    print '*'*80
    print '*', '\033[93m'+'SOJO RUNNING', '\033[0m'
    print '*'
    print '*', 'open', '\033[92m'+'http://' + ip + ':' + str(self._port) + '/c/sojo/' + '\033[0m'
    print '*'*80

    tornado.ioloop.IOLoop.instance().start()

  def close(self, signal, frame):
    '''
    '''

    print 'Sayonara!'
    sys.exit(0)
