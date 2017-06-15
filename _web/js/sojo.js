var S = S || {};
S.history = [];
S.current_synapse_id = -1;
S.current_synapse_center = [0,0,0];
S.current_pre_synaptic_neuron = -1;
S.dojo = 'https://dojo.rc.fas.harvard.edu/dojo/'

S.load_synapse = function() {
  
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '../?image');
  xhr.onload = S.synapse_loaded;
  xhr.responseType = 'arraybuffer';
  xhr.send(null);

};

S.synapse_loaded = function(e) {

  var response = e.target.response;

  // grab meta data
  var meta = new Float64Array(response.slice(0,6*8));

  var blob = new Blob([response.slice(6*8,-1)], {type: "image/jpeg"});

  // update meta
  document.getElementById('meta').innerHTML = '<b>Synapse ID:</b> ' + meta[0] + '<br>';
  document.getElementById('meta').innerHTML += '<b class="red">Pre-synaptic Neuron:</b> ' + meta[1] + '<br>';
  document.getElementById('meta').innerHTML += '<b class="green">Post-synaptic Neuron:</b> ' + meta[2] + '<br>';
  document.getElementById('meta').innerHTML += '<b>X, Y, Z:</b> (' + meta[3] + ', ' + meta[4] + ', ' + meta[5] + ')<br>';

  // update image
  document.getElementById('image').setAttribute('src',URL.createObjectURL(blob))

  S.current_synapse_id = meta[0];
  S.current_synapse_center = [meta[3], meta[4], meta[5]];
  S.current_pre_synaptic_neuron = meta[1];

};

S.proofread_synapse = function(how, e) {

  S.history.push(S.current_synapse_id);

  S.load_synapse();

  // enable back button
  document.getElementById('back').classList = ['grayButton'];
  document.getElementById('back').onclick = S.go_back.bind(this, 'back');

  document.getElementById('skip').classList = ['grayButton'];
  document.getElementById('skip').onclick = S.proofread_synapse.bind(this, 'skip');  

};

S.go_back = function() {

  var old_id = S.history.pop();

  if (S.history.length == 1) {
    document.getElementById('back').classList = ['grayButton disabled'];
    document.getElementById('back').onclick = null;    
  }

  document.getElementById('skip').classList = ['grayButton disabled'];
  document.getElementById('skip').onclick = null;  

};

S.start_dojo = function() {

  var coordinates = S.current_synapse_center;

  window.open(S.dojo+'/?jump='+coordinates[0]+','+coordinates[1]+','+coordinates[2]+'&activeId='+S.current_pre_synaptic_neuron, 'dojo');

};