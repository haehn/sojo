var S = S || {};

S.load_synapse = function() {
  
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '../?image');
  xhr.onload = S.synapse_loaded.bind(xhr);
  xhr.responseType = 'arraybuffer';
  xhr.send(null);

};

S.synapse_loaded = function(e) {

  response = e.target.result;

  // grab meta data
  meta = new Float64Array(response.slice(6*8,-1));
  console.log(meta);

  blob = new Blob([response.slice(6*8,-1)], {type: "image/jpeg"});
  document.getElementById('image').setAttribute('src',URL.createObjectURL(blob))

};