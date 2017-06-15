#!/usr/bin/env python
import sys


import _sojo

def print_help( scriptName ):
  '''
  '''
  description = ''
  print description
  print
  print 'Usage: ' + scriptName + ' OUT_DIR PORT SYNAPSE_CONNECTIONS.JSON IMAGES.JSON LABELS.JSON'
  print 'Example:'
  print '  ' + scriptName + ' /tmp/aaa/ 8000 /n/coxfs01/leek/results/2017-05-11_R0/synapse-connections.json /n/coxfs01/leek/data/ECS_iarpa201610_100um_100um_100um.json /n/coxfs01/leek/results/2017-05-11_R0/boss/boss.json'

#
# entry point
#
if __name__ == "__main__":

  # always show the help if no arguments were specified
  if len(sys.argv) != 6:
    print_help( sys.argv[0] )
    sys.exit( 1 )

  output_dir = sys.argv[1]
  port = sys.argv[2]
  synapse_connections_json = sys.argv[3]
  images_json = sys.argv[4]
  labels_json = sys.argv[5]


  manager = _sojo.Manager(output_dir)
  manager.start(synapse_connections_json, images_json, labels_json)

  webserver = _sojo.Webserver(manager, port)
  webserver.start()
