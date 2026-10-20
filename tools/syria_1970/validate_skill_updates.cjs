/* Validate unchanged skill metadata, bounded edits and local references. */
const fs = require('fs'), path = require('path');
const stage = path.join(__dirname, 'skill_updates');
const source = 'C:/Users/sonyz/.codex/skills';
const files = JSON.parse(fs.readFileSync(path.join(stage, 'manifest.json'), 'utf8'));
const errors = [];
for (const {relative} of files) {
  const text = fs.readFileSync(path.join(stage, relative), 'utf8');
  if (relative.endsWith('SKILL.md')) {
    const front = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!front) { errors.push(relative+': missing frontmatter'); continue; }
    const original = fs.readFileSync(path.join(source, relative), 'utf8').replace(/^\uFEFF/, '').match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!original || front[1].replace(/\r/g, '') !== original[1].replace(/\r/g, '')) errors.push(relative+': unrequested frontmatter change');
    const meta = Object.fromEntries(front[1].split(/\r?\n/).filter(Boolean).map(line => {
      const match = line.match(/^([\w-]+): (.+)$/);
      if (!match) throw new Error('This narrow validator only supports unchanged flat metadata: '+relative);
      return [match[1], match[2]];
    }));
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(meta.name) || meta.name.length > 64) errors.push(relative+': invalid name');
    if (typeof meta.description !== 'string' || !meta.description.length || meta.description.length > 1024 || /[<>]/.test(meta.description)) errors.push(relative+': invalid description');
    for (const key of Object.keys(meta)) if (!['name', 'description', 'license', 'allowed-tools', 'metadata'].includes(key)) errors.push(relative+': unexpected '+key);
  }
  if (/^\s*\[TODO:[^\n]*\]\s*$/m.test(text)) errors.push(relative+': unfinished scaffold');
  for (const match of text.matchAll(/\]\(([^)]+\.md)(?:#[^)]*)?\)/g)) {
    if (/^https?:/.test(match[1])) continue;
    const rel = path.join(path.dirname(relative), match[1]);
    if (!fs.existsSync(path.join(stage, rel)) && !fs.existsSync(path.join(source, rel))) errors.push(relative+': missing '+match[1]);
  }
}
const result = {status: errors.length ? 'FAIL' : 'PASS', files_checked: files.length, errors, note: 'Existing flat metadata unchanged; names, descriptions, scaffolds and local links checked. Official quick_validate.py could not run because its Python environment lacks PyYAML.'};
fs.writeFileSync(path.join(stage, 'validation.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result));
process.exitCode = errors.length ? 1 : 0;
