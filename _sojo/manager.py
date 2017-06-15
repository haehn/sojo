import numpy as np
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

  def get_synapse(self, idx):
    '''
    '''
    xx = int(self._x_s[idx])
    yy = int(self._y_s[idx])
    zz = int(self._z_s[idx])

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

    return blended

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

      blended_image = self.get_synapse(random_id)
      output = StringIO.StringIO()
      blended_image.save(output, 'JPEG')

      content_type = 'image/jpeg'
      content = output.getvalue()
      ####



    return content, content_type

