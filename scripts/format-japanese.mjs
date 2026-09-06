// Add optional Japanese phrase breaks at build time. No text or browser JS is
// added. Inline emphasis, links, IDs, metadata and existing line breaks survive.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parse, serialize, defaultTreeAdapter as tree } from 'parse5';
import { loadDefaultJapaneseParser } from 'budoux';

const parser = loadDefaultJapaneseParser();
const words = new Intl.Segmenter('ja', { granularity: 'word' });
const blocks = new Set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'dt', 'dd', 'td', 'th', 'figcaption']);
const excluded = new Set(['pre', 'code', 'script', 'style', 'svg', 'math', 'textarea', 'button', 'select']);
const htmlNS = 'http://www.w3.org/1999/xhtml';
const attr = (node, name) => node.attrs?.find(a => a.name === name)?.value;
const children = node => node.tagName === 'template' ? node.content.childNodes : node.childNodes || [];
const hasClass = (node, name) => (attr(node, 'class') || '').split(/\s+/).includes(name);
const japanese = text => /[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]/u.test(text);

export function boundaries(text) {
  // BudouX finds phrases; ICU's word boundaries prevent model suggestions such
  // as 「お問い|合わせ」「相|手」 from splitting an actual word.
  const wordStarts = new Set([...words.segment(text)].map(item => item.index));
  let offset = 0;
  return parser.parse(text).slice(0, -1).map(phrase => (offset += phrase.length))
    .filter(index => wordStarts.has(index)
      && !/[（「『【〈《“‘(\[・]$/u.test(text.slice(0, index))
      && !/^[、。，．？！：；）」』】〉》”’!?;:),\]・]/u.test(text.slice(index)));
}

function formatBlock(node) {
  const groups = [[]];
  let nestedBlock = false;
  function collect(current) {
    if (current !== node && hasClass(current, 'jp-text')) { nestedBlock = true; return; }
    if (current !== node && blocks.has(current.tagName)) { nestedBlock = true; return; }
    const differentLanguage = current !== node && attr(current, 'lang') && !/^ja(?:-|$)/i.test(attr(current, 'lang'));
    if (excluded.has(current.tagName) || hasClass(current, 'heading-phrase') || current.tagName === 'br' || differentLanguage) {
      if (groups.at(-1).length) groups.push([]);
      return;
    }
    if (current.nodeName === '#text') groups.at(-1).push(current);
    for (const child of children(current)) collect(child);
  }
  collect(node);
  // Leaf blocks own the typography. Parent list items with nested paragraphs
  // must not reformat their already processed descendants.
  if (nestedBlock || !groups.some(group => japanese(group.map(n => n.value).join('')))) return false;
  let formatted = false;
  for (const group of groups) {
    const text = group.map(n => n.value).join('');
    if (!japanese(text)) continue;
    const breaks = boundaries(text);
    let start = 0;
    for (const original of group) {
      const end = start + original.value.length;
      const positions = breaks.filter(index => index > start && index <= end).map(index => index - start);
      let previous = 0;
      for (const position of positions) {
        if (position > previous) tree.insertBefore(original.parentNode, {
          nodeName: '#text', value: original.value.slice(previous, position), parentNode: null,
        }, original);
        tree.insertBefore(original.parentNode, tree.createElement('wbr', htmlNS, []), original);
        previous = position;
      }
      if (positions.length) { original.value = original.value.slice(previous); formatted = true; }
      start = end;
    }
  }
  // Even short text without a candidate benefits from word preservation.
  const classes = attr(node, 'class');
  if (classes !== undefined) node.attrs.find(a => a.name === 'class').value += ' jp-text';
  else node.attrs.push({ name: 'class', value: 'jp-text' });
  return formatted;
}

export function formatHTML(source) {
  const document = parse(source);
  let count = 0;
  function visit(node, language = '', inContent = false) {
    language = attr(node, 'lang') || language;
    inContent ||= node.tagName === 'main' || node.tagName === 'footer';
    if (excluded.has(node.tagName) || hasClass(node, 'jp-text')) return;
    for (const child of children(node)) visit(child, language, inContent);
    const additional = ['resource-title', 'resource-description'].some(name => hasClass(node, name));
    if (inContent && /^ja(?:-|$)/i.test(language) && (blocks.has(node.tagName) || additional)) {
      if (formatBlock(node)) count++;
    }
  }
  visit(document);
  return { html: serialize(document), count };
}

async function formatDirectory(directory) {
  let pages = 0, blocks = 0;
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      const result = await formatDirectory(filename); pages += result.pages; blocks += result.blocks;
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      const source = await fs.readFile(filename, 'utf8');
      const result = formatHTML(source);
      if (result.html !== source) await fs.writeFile(filename, result.html);
      pages++; blocks += result.count;
    }
  }
  return { pages, blocks };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const result = await formatDirectory(path.resolve(process.argv[2] || 'public'));
  console.log(`Japanese typography: ${result.blocks} text blocks across ${result.pages} HTML pages; no client script.`);
}
