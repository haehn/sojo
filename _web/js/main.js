window.onload = function() {

  // callbacks
  document.getElementById('skip').onclick = S.proofread_synapse.bind(this, 'skip');
  document.getElementById('good').onclick = S.proofread_synapse.bind(this, 'good');
  document.getElementById('bad').onclick = S.proofread_synapse.bind(this, 'bad');

  document.getElementById('dojo').onclick = S.proofread_synapse.bind(this, 'bad');

  S.load_synapse();
  
};