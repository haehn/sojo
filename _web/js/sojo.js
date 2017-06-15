var S = S || {};

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

};

S.proofread_synapse = function(how, e) {

  console.log(how);

  S.load_synapse();

};