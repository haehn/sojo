var S = S || {};

S.load_synapse = function() {
  
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '../?image');
  xhr.onload = S.synapse_loaded.bind(xhr);
  xhr.responseType = 'arraybuffer';
  xhr.send(null);

};

S.synapse_loaded = function(xhr) {
  
  console.log(xhr)
  XXX = xhr;

};