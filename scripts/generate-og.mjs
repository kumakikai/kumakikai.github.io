#!/usr/bin/env node
// Optional authoring utility. The generated PNGs are committed; site builds do not run this script.
// Provide sharp through NODE_PATH or an existing local installation. No package install is performed.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.env.XDG_CACHE_HOME ||= path.join(os.tmpdir(), 'kumakikai-og-cache');
await fs.mkdir(process.env.XDG_CACHE_HOME, { recursive: true });
const require = createRequire(import.meta.url);
let sharp;
try {
  sharp = require('sharp');
} catch {
  throw new Error('This optional asset tool needs sharp. Set NODE_PATH to an existing node_modules directory containing sharp, then run node scripts/generate-og.mjs.');
}

const apps = JSON.parse(await fs.readFile(path.join(root, 'data/apps.json'), 'utf8'));
const copy = JSON.parse(await fs.readFile(path.join(root, 'data/home/ja.json'), 'utf8'));
const output = path.join(root, 'static/images/og');
await fs.mkdir(output, { recursive: true });
const width = 1200;
const height = 630;
const family = 'Hiragino Sans, Noto Sans CJK JP, Yu Gothic, sans-serif';
const ink = '#17202d';
const muted = '#516174';
const escape = (value) => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[char]));
const text = (value, x, y, size, weight = 500, color = ink, extra = '') =>
  `<text x="${x}" y="${y}" font-family="${family}" font-size="${size}" font-weight="${weight}" fill="${color}" ${extra}>${escape(value)}</text>`;
const svg = (body) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><rect width="1200" height="630" fill="#f7f9fc"/>${body}</svg>`);

async function icon(app, size) {
  const source = path.join(root, 'static', app.icon.replace(/^\//, ''));
  const radius = Math.round(size * 0.2);
  const mask = Buffer.from(`<svg width="${size}" height="${size}"><rect width="${size}" height="${size}" rx="${radius}" fill="white"/></svg>`);
  return sharp(source).resize(size, size, { fit: 'contain', withoutEnlargement: true }).composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
}

async function save(name, background, overlays) {
  const destination = path.join(output, `${name}.png`);
  await sharp(background).composite(overlays).png({ compressionLevel: 9, palette: true, quality: 95, effort: 10, colours: 256 }).toFile(destination);
  const metadata = await sharp(destination).metadata();
  if (metadata.width !== width || metadata.height !== height) throw new Error(`Incorrect image dimensions: ${name}`);
  const { size } = await fs.stat(destination);
  console.log(`${name}.png: ${width}x${height}, ${Math.round(size / 1024)} KiB`);
}

const common = [
  '<rect x="686" y="135" width="452" height="328" rx="36" fill="#eaf0f8"/>',
  text('KUMAKIKAI', 72, 150, 70, 700, ink, 'letter-spacing="-1.4"'),
  ...copy.heroLines.map((line, index) => text(line, 76, 245 + index * 66, 42, 600)),
  '<path d="M76 490H1124" stroke="#d7dfe9" stroke-width="2"/>',
  text('iPhone & iPad Apps', 76, 548, 27, 500, muted),
  text('kumakikai.github.io', 1124, 548, 22, 400, muted, 'text-anchor="end"')
].join('');
const commonIcons = [];
for (const [index, app] of apps.entries()) {
  commonIcons.push({ input: await icon(app, 88), left: 710 + (index % 4) * 108, top: 190 + Math.floor(index / 4) * 130 });
}
await save('default', svg(common), commonIcons);

for (const app of apps) {
  const local = copy.apps[app.id];
  const tagline = local.taglineLines || [];
  const nameSize = local.name.length > 13 ? 66 : 78;
  const background = [
    text('KUMAKIKAI', 76, 91, 28, 700, ink, 'letter-spacing="2"'),
    '<rect x="819" y="151" width="314" height="314" rx="40" fill="#eaf0f8"/>',
    text(local.name, 76, tagline.length ? 226 : 282, nameSize, 700, ink, 'letter-spacing="-1"'),
    ...tagline.map((line, index) => text(line, 76, 325 + index * 68, 47, 600)),
    '<path d="M76 506H1124" stroke="#d7dfe9" stroke-width="2"/>',
    text(local.platform, 76, 562, 26, 500, muted),
    text(app.status === 'development' ? copy.development : 'kumakikai.github.io', 1124, 562, 24, 500, muted, 'text-anchor="end"')
  ].join('');
  await save(app.id, svg(background), [{ input: await icon(app, 232), left: 860, top: 192 }]);
}
