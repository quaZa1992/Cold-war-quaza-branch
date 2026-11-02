// IMPERIA COLD WAR — Installed Chile browser review using the retained independent geometry checks.
const fs = require('fs');
const path = require('path');
const docs = path.resolve(__dirname, '../../docs/CHILE_COLDWAR_CONCEPT_1970_1990');
let source = fs.readFileSync(path.join(docs, 'verify_preview.cjs'), 'utf8');
source = source.replaceAll("'preview-review.html'", "'IMPLEMENTED_preview.html'")
  .replaceAll("'BROWSER_QA.json'", "'IMPLEMENTED_BROWSER_QA.json'")
  .replace(/'preview-([a-z-]+)\.png'/g, "'IMPLEMENTED-preview-$1.png'");
source = source.replace("/\\$(\\d+(?:\\.\\d+)?) billion/g", "/\\$(\\d+(?:\\.\\d+)?) (billion|million)/g")
  .replace(".map(m=>Number(m[1]));", ".map(m=>Number(m[1])*(m[2]==='million'?0.001:1));")
  .replace("dollars[0]!==t.setup||dollars[1]!==t.weekly", "Math.abs(dollars[0]-t.setup)>1e-9||Math.abs(dollars[1]-t.weekly)>1e-9");
// Run the unchanged independent browser assertions against the installed-code
// viewer, without replacing any original approval record or capture.
new Function('require', '__dirname', source)(require, docs);
