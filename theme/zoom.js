/* ================================================================
   Font Zoom Control — The Architecture of Intent
   Adds a persistent +/- zoom widget. Saves preference to localStorage.
   ================================================================ */

(function () {
  var BASE = 19;
  var MIN  = 14;
  var MAX  = 28;
  var STEP = 1;
  var KEY  = 'aoi-font-size';

  function getSize() {
    var stored = parseInt(localStorage.getItem(KEY), 10);
    return (!isNaN(stored) && stored >= MIN && stored <= MAX) ? stored : BASE;
  }

  function applySize(px) {
    document.documentElement.style.setProperty('font-size', px + 'px', 'important');
    document.body.style.setProperty('font-size', px + 'px', 'important');
    localStorage.setItem(KEY, px);
    if (label) label.textContent = px + 'px';
  }

  // Build the widget
  var widget = document.createElement('div');
  widget.id = 'zoom-widget';
  widget.setAttribute('aria-label', 'Font size controls');
  widget.innerHTML =
    '<button id="zoom-out" title="Decrease font size" aria-label="Decrease font size">A−</button>' +
    '<span id="zoom-label">' + getSize() + 'px</span>' +
    '<button id="zoom-in"  title="Increase font size" aria-label="Increase font size">A+</button>';

  var style = document.createElement('style');
  style.textContent = [
    '#zoom-widget {',
    '  position: fixed;',
    '  bottom: 1.5rem;',
    '  right: 1.5rem;',
    '  z-index: 9999;',
    '  display: flex;',
    '  align-items: center;',
    '  gap: 2px;',
    '  background: rgba(15, 23, 42, 0.82);',
    '  border: 1px solid rgba(148, 163, 184, 0.18);',
    '  border-radius: 999px;',
    '  padding: 4px 10px;',
    '  backdrop-filter: blur(8px);',
    '  box-shadow: 0 4px 24px rgba(0,0,0,0.4);',
    '  user-select: none;',
    '}',
    '#zoom-widget button {',
    '  background: none;',
    '  border: none;',
    '  color: rgba(148, 163, 184, 0.85);',
    '  font-size: 13px;',
    '  font-weight: 600;',
    '  cursor: pointer;',
    '  padding: 3px 8px;',
    '  border-radius: 999px;',
    '  line-height: 1;',
    '  transition: color 0.15s, background 0.15s;',
    '}',
    '#zoom-widget button:hover {',
    '  color: #fff;',
    '  background: rgba(255,255,255,0.08);',
    '}',
    '#zoom-label {',
    '  font-size: 11px;',
    '  color: rgba(148, 163, 184, 0.55);',
    '  min-width: 36px;',
    '  text-align: center;',
    '  font-family: monospace;',
    '}',
  ].join('\n');

  document.head.appendChild(style);

  function init() {
    document.body.appendChild(widget);

    var label   = document.getElementById('zoom-label');
    var btnIn   = document.getElementById('zoom-in');
    var btnOut  = document.getElementById('zoom-out');
    var current = getSize();

    function applySize(px) {
      document.documentElement.style.setProperty('font-size', px + 'px', 'important');
      document.body.style.setProperty('font-size', px + 'px', 'important');
      localStorage.setItem(KEY, px);
      if (label) label.textContent = px + 'px';
      current = px;
    }

    applySize(current);

    btnIn.addEventListener('click', function () {
      if (current < MAX) applySize(current + STEP);
    });

    btnOut.addEventListener('click', function () {
      if (current > MIN) applySize(current - STEP);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
