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
  console.log(meta);

  var blob = new Blob([response.slice(6*8,-1)], {type: "image/jpeg"});
  document.getElementById('image').setAttribute('src',URL.createObjectURL(blob))

};