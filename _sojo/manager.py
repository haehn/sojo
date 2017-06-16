import numpy as np
import os
from PIL import Image
import StringIO

from util import Util

class Manager():
  '''
  '''
  def __init__(self, outdir):
    '''
    '''
    self._outdir = outdir

  def start(self, synapse_connections_json, images_json, labels_json):
    '''
    '''
    # load JSONS
    n1, n2, x_s, y_s, z_s = Util.load_synapse_connections(synapse_connections_json)
    self._pre_neurons = n1
    self._post_neurons = n2
    self._x_s = x_s
    self._y_s = y_s
    self._z_s = z_s

    self._bidx = Util.load_images_json(images_json)

    self._tiles = Util.load_labels_json(labels_json)
    # done loading

    self._seen_ids = []
    self._proofread_ids_good = {}
    self._proofread_ids_bad = {}

    # check if we can load data
    if os.path.exists(self._manager._outdir):

      with open(self._manager._outdir + '/seenids.p', 'rb') as f:
        self._manager._seen_ids = pickle.load(f)
      with open(self._manager._outdir + '/goodids.p', 'rb') as f:
        self._manager._proofread_ids_good = pickle.load(f)
      with open(self._manager._outdir + '/badids.p', 'rb') as f:
        self._manager._proofread_ids_bad = pickle.load(f)    

      print 'Loaded', len(self._seen_ids), 'proofread synapses..'  

  def get_synapse(self, idx, debug=False):
    '''
    '''

    n1 = self._pre_neurons[idx]
    n2 = self._post_neurons[idx]
    x = self._x_s[idx]
    y = self._y_s[idx]
    z = self._z_s[idx]

    if debug:
      print 'loading debug image /tmp/test.jpeg'
      import cv2
      blended = cv2.imread('/tmp/test.jpeg')
      blended = Image.fromarray(blended)

    else:

      xx = int(x)
      yy = int(y)
      zz = int(z)

      image = Util.cut_image(self._bidx, xx-512, yy-512, zz, 1024, 1024)
      seg = Util.cut_labels(self._tiles, xx-512, yy-512, zz, 1024, 1024)

      # create RGBA label overlay of pre- and post-synaptic neuron
      # red is pre
      # green is post
      overlay = np.zeros((1024, 1024, 3), dtype=np.uint8)
      overlay[seg == self._pre_neurons[idx], 0] = 255
      #overlay[seg == self._pre_neurons[idx], 3] = .3
      overlay[seg == self._post_neurons[idx], 1] = 255
      #overlay[seg == self._post_neurons[idx], 3] = .3

      image_ = Image.fromarray(image)
      image_ = image_.convert('RGBA')
      overlay_ = Image.fromarray(overlay)
      overlay_ = overlay_.convert('RGBA')

      blended = Image.blend(image_, overlay_, 0.3)

    return blended, n1, n2, x, y, z

  def get(self, request):
    '''
    '''
    splitted_request = request.uri.split('/')

    content = u'Error'
    content_type = 'text/html'

    if splitted_request[1] == '?image':
      ### show next random synapse
      random_id = np.random.randint(0, len(self._pre_neurons))
      while random_id in self._seen_ids:
        random_id = np.random.randint(0, len(self._pre_neurons))

      blended_image, n1, n2, x, y, z = self.get_synapse(random_id, debug=(len(splitted_request) > 2 and splitted_request[2] == 'debug'))
      output = StringIO.StringIO()
      blended_image.save(output, 'JPEG')

      meta = np.zeros((9), dtype=np.float64)
      meta[0] = random_id
      meta[1] = n1
      meta[2] = n2
      meta[3] = int(x)
      meta[4] = int(y)
      meta[5] = int(z)
      meta[6] = len(self._proofread_ids_good.keys())
      meta[7] = len(self._proofread_ids_bad.keys())
      meta[8] = len(self._pre_neurons)

      content_type = 'image/jpeg'
      content = meta.tobytes() + output.getvalue()
      ####

    elif splitted_request[1] == '?proofread':

      synapse_id = splitted_request[2]
      result = splitted_request[3]

      if result == 'good':
        
        self._proofread_ids_good[synapse_id] = result

        self._seen_ids.append(synapse_id)

      elif result == 'bad':

        self._proofread_ids_bad[synapse_id] = result

        self._seen_ids.append(synapse_id)

      else:

        print 'skipped', synapse_id    

      content_type = 'text/html'
      content = 'thanks'

    return content, content_type

