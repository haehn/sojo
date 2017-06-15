import cv2
import json
import numpy as np
import tifffile

class Util:
  '''
  Most code from @leek's ipy (just fixed some bugs and cleaned up)
  '''

  @staticmethod
  def load_synapse_connections(path):
    '''
    '''
    sdict = json.load(open(path))
    n1, n2 = [np.array(sdict[k]) for k in "neuron_1", "neuron_2"]
    x, y, z = [np.array(sdict["synapse_center"][k]) for k in "xyz"]

    return n1, n2, x, y, z

  @staticmethod
  def load_images_json(path):
    '''
    '''
    bidx = json.load(open(path))
    bidx.keys()

    return bidx

  @staticmethod
  def load_labels_json(path):
    '''
    '''
    tiles = {}
    for tile in json.load(open(path))["tiles"]:
      tiles[tile["row"], tile["column"], tile["z"]] = tile["location"]

    return tiles

  @staticmethod
  def cut_image(bidx, x, y, z, width, height):
    '''
    '''
    col0 = max(x,0) / 1024
    col1 = (x+width+1023) / 1024
    
    row0 = max(y,0) / 1024
    row1 = (y+height+1023) / 1024
    result = np.zeros((height, width), np.uint8)
    pattern = bidx["sections"][z]
    
    for col in range(col0, col1):
      for row in range(row0, row1):
        x0 = max(0,max(x, col * 1024))
        x1 = min(x + width, (col+1) * 1024)
        y0 = max(0,max(y, row * 1024))
        y1 = min(y + height, (row+1) * 1024)
        #print x0,y0,x1,y1, pattern, row,col

        plane = cv2.imread(pattern.format(z=z, row=row+1, column=col+1), cv2.IMREAD_GRAYSCALE)

        result[y0-y:y1-y, x0-x:x1-x] = plane[y0-row * 1024: y1 - row * 1024,x0-col * 1024:x1-col *1024]

    return result

  @staticmethod
  def cut_labels(tiles, x, y, z, width, height):
    '''
    '''
    col0 = max(x,0) / 2048
    col1 = (x+width+2047) / 2048
    row0 = max(y,0) / 2048
    row1 = (y+height+2047) / 2048
    result = np.zeros((height, width), np.uint32)
    for col in range(col0, col1):
        for row in range(row0, row1):
            x0 = max(0,max(x, col * 2048))
            x1 = min(x + width, (col+1) * 2048)
            y0 = max(0,max(y, row * 2048))
            y1 = min(y + height, (row+1) * 2048)
            plane = tifffile.imread(tiles[row, col, z])
            #print 'loading', tiles[row, col, z]
            result[y0-y:y1-y, x0-x:x1-x] = plane[y0-row * 2048: y1 - row * 2048,
                                                 x0-col * 2048:x1-col *2048]
    return result
