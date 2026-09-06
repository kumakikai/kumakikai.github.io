import assert from 'node:assert/strict';
import { parse } from 'parse5';
import { formatHTML, boundaries } from './format-japanese.mjs';

function snapshot(source) {
  const result = { text: '', attributes: [] };
  function visit(node) {
    if (node.nodeName === '#text') result.text += node.value;
    for (const attr of node.attrs || []) if (attr.name !== 'class') result.attributes.push([node.tagName, attr.name, attr.value]);
    for (const child of node.tagName === 'template' ? node.content.childNodes : node.childNodes || []) visit(child);
  }
  visit(parse(source));
  return result;
}
const input = `<!doctype html><html lang="ja"><head><title>お問い合わせ</title><script type="application/ld+json">{"name":"相手に伝える"}</script></head><body><main>
<h1 id="backup">使い始めは、<strong>バックアップ</strong>を取り込むだけ。</h1>
<p>端末を挟んだ相手にも字幕を表示。<a href="/support/?q=日本語#連絡">お問い合わせください。</a></p>
<p>Apple Watchから「喫煙」「我慢」を記録。<br>当日の記録も確認。</p>
<ul><li><p>問題集を作成します。</p><ul><li>試験勉強に使えます。</li></ul></li></ul>
<template><article><h2>テレビの声も、身近な人との会話も。</h2><p>ウィジェットでコードをコピー。</p></article></template>
<p lang="en">Use <strong>Apple Watch</strong> to record.</p><pre><code>const title = "お問い合わせ";</code></pre>
<p>表示言語を確認。<span lang="en">お問い合わせを確認。</span>設定に戻ります。</p>
</main><footer><p class="footer-trademarks">AppleとAppleのロゴは、Apple Inc.の商標です。</p></footer></body></html>`;
const output = formatHTML(input).html;
assert.deepEqual(snapshot(output), snapshot(input), 'Visible text, link targets, IDs and metadata must be unchanged');
assert.equal(formatHTML(output).html, output, 'Formatting must be idempotent');
assert(output.includes('<template><article><h2 class="jp-text">'), 'Inert random candidates must also be formatted');
assert(output.includes('<p class="footer-trademarks jp-text">'), 'Footer Japanese shares the body typography rules');
assert(output.includes('<p lang="en">Use <strong>Apple Watch</strong> to record.</p>'));
assert(output.includes('<span lang="en">お問い合わせを確認。</span>'));
assert(output.includes('<pre><code>const title = "お問い合わせ";</code></pre>'));
for (const [text, word] of [
  ['困ったときはお問い合わせください。', '問い合わせ'],
  ['端末を挟んだ相手にも字幕を表示します。', '相手'],
  ['使い始めは、バックアップを取り込むだけ。', 'バックアップ'],
  ['ウィジェットからすぐに記録。', 'ウィジェット'],
  ['iPhone・iPad向けのアプリを企画・開発・運営しています。', '企画・開発・運営'],
]) {
  const start = text.indexOf(word);
  assert(!boundaries(text).some(index => index > start && index < start + word.length), `Do not split ${word}`);
}
console.log('Japanese typography: text/URL/metadata preservation, nested markup, template candidates, excluded code/languages, idempotence and word boundaries PASS.');
