import { readFile, writeFile, mkdir, cp } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { Marked } from "marked";
import markedKatex from "marked-katex-extension";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const source = path.join(root, "公理：数学史与哲学", "英文版本");
const output = path.join(root, "writing", "axioms");
const assets = path.join(root, "assets", "vendor", "katex");
const articles = [
  { file: "00-introduction.md", url: "0.html", number: "00", label: "Introduction" },
  { file: "1-1.md", url: "1-1.html", number: "1.1", label: "Article 1.1 · From Infinity to Axioms" },
  { file: "1-2.md", url: "1-2.html", number: "1.2", label: "Article 1.2 · From Infinity to Axioms" },
  { file: "1-3.md", url: "1-3.html", number: "1.3", label: "Article 1.3 · From Infinity to Axioms" },
  { file: "1-4.md", url: "1-4.html", number: "1.4", label: "Article 1.4 · From Infinity to Axioms" },
  { file: "1-5.md", url: "1-5.html", number: "1.5", label: "Article 1.5 · From Infinity to Axioms" },
  { file: "1-6.md", url: "1-6.html", number: "1.6", label: "Article 1.6 · From Infinity to Axioms" },
];

const escapeHtml = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const slug = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function makeToc(headings) {
  const groups = [];
  for (const heading of headings) {
    if (heading.level === 2) groups.push({ ...heading, children: [] });
    else if (groups.length) groups.at(-1).children.push(heading);
  }
  return groups.map((group, index) => {
    const children = group.children.length
      ? '<div class="toc-children" id="toc-group-' + index + '"' + (index === 0 ? "" : " inert") + '><ol>' +
        group.children.map((child) => '<li><a href="#' + child.id + '">' + escapeHtml(child.text) + '</a></li>').join("") + '</ol></div>'
      : "";
    const parent = group.children.length
      ? '<button type="button" class="toc-parent" aria-expanded="' + (index === 0 ? "true" : "false") +
        '" aria-controls="toc-group-' + index + '" data-target="' + group.id + '"><span>' +
        escapeHtml(group.text) + '</span><span class="toc-chevron" aria-hidden="true">⌄</span></button>'
      : '<a class="toc-parent toc-link" href="#' + group.id + '">' + escapeHtml(group.text) + '</a>';
    return '<li class="toc-group' + (index === 0 ? " is-open" : "") + '">' + parent + children + '</li>';
  }).join("");
}

const template = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="@@DECK@@">
  <title>@@TITLE@@ — Axioms — Jiankun (Kevin) Xu</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&amp;family=Manrope:wght@400;500;600;700&amp;family=Newsreader:opsz,wght@6..72,400;6..72,500&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../styles.css">
  <link rel="stylesheet" href="../../assets/vendor/katex/katex.min.css">
  <link rel="stylesheet" href="reader.css">
  <script src="reader.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header detail-header reader-header">
    <a class="wordmark" href="../../index.html">Jiankun (Kevin) Xu</a>
    <nav class="site-nav" aria-label="Primary navigation">
      <a href="../../index.html#about">About</a>
      <a href="../../index.html#academic">Academic Work</a>
      <a href="../../index.html#thinking">Thinking</a>
      <a href="../../index.html#writing">Writing</a>
      <a href="../../index.html#beyond">Beyond</a>
      <a href="../../index.html#resume">Résumé</a>
    </nav>
    <a class="back-link" href="index.html">← Axioms</a>
  </header>
  <main class="reader-main" id="main">
    <div class="reader-topline"><a href="../index.html">Writing &amp; Reading</a><span aria-hidden="true">/</span><a href="index.html">Axioms</a><span aria-hidden="true">/</span><span>@@LABEL@@</span></div>
    <div class="reader-layout">
      <aside class="reader-sidebar" aria-label="Article navigation">
        <button class="toc-mobile-toggle" type="button" aria-controls="reader-toc" aria-expanded="false">Contents <span aria-hidden="true">⌄</span></button>
        <nav class="reader-toc" id="reader-toc" aria-label="On this page">
          <p class="micro-label">In this article</p>
          <ol class="toc-list">@@TOC@@</ol>
          <a class="toc-series-link" href="index.html">All articles ↗</a>
        </nav>
      </aside>
      <article class="reader-article">
        <header class="reader-article-header">
          <p class="eyebrow">@@LABEL@@</p>
          <h1>@@TITLE@@</h1>
          <p class="reader-deck">@@DECK@@</p>
        </header>
        <div class="reader-prose">@@BODY@@</div>
        <nav class="reader-pagination" aria-label="Article sequence">@@PREVIOUS@@@@NEXT@@</nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><p>Jiankun (Kevin) Xu <span aria-hidden="true">·</span> Axioms</p><a href="mailto:kevinxu703@gmail.com">kevinxu703@gmail.com</a></footer>
</body>
</html>
`;

function articlePage(article, markdown, previousArticle, nextArticle) {
  const cleaned = markdown.replace(/^<!--[\s\S]*?-->\s*/, "").trim();
  const match = cleaned.match(/^# (.+)\n\n\*(.+)\*\n\n/);
  if (!match) throw new Error(article.file + " needs a title and italic deck.");
  const [ , title, deck ] = match;
  const body = cleaned.slice(match[0].length);
  const headings = [...body.matchAll(/^(#{2,3}) (.+)$/gm)].map((item) => ({
    level: item[1].length, text: item[2], id: slug(item[2])
  }));
  if (new Set(headings.map((heading) => heading.id)).size !== headings.length) {
    throw new Error(article.file + " has duplicate heading IDs.");
  }
  let headingIndex = 0;
  const parser = new Marked(markedKatex({ throwOnError: true, output: "htmlAndMathml" }));
  parser.use({ renderer: {
    heading({ tokens, depth }) {
      const heading = headings[headingIndex++];
      if (!heading || heading.level !== depth) throw new Error("Heading order mismatch.");
      return '<h' + depth + ' id="' + heading.id + '">' + this.parser.parseInline(tokens) + '</h' + depth + '>\n';
    },
    link({ href, title, tokens }) {
      const external = /^https?:\/\//.test(href);
      return '<a href="' + escapeHtml(href) + '"' +
        (title ? ' title="' + escapeHtml(title) + '"' : "") +
        (external ? ' target="_blank" rel="noopener noreferrer"' : "") +
        '>' + this.parser.parseInline(tokens) + '</a>';
    }
  }});
  const rendered = parser.parse(body);
  const previous = previousArticle
    ? '<a href="' + previousArticle.url + '"><small>Previous</small><span>' +
      escapeHtml(previousArticle.number === "00" ? "Introduction" : previousArticle.number + " · " + previousArticle.title) + '</span></a>'
    : '<span class="reader-nav-empty"></span>';
  const next = nextArticle
    ? '<a href="' + nextArticle.url + '"><small>Next</small><span>' +
      escapeHtml(nextArticle.number + " · " + nextArticle.title) + '</span></a>'
    : '<span class="reader-nav-empty"></span>';
  const replacements = {
    "@@TITLE@@": escapeHtml(title), "@@DECK@@": escapeHtml(deck),
    "@@LABEL@@": escapeHtml(article.label), "@@BODY@@": rendered,
    "@@TOC@@": makeToc(headings), "@@PREVIOUS@@": previous, "@@NEXT@@": next
  };
  return Object.entries(replacements).reduce((html, [key, value]) => html.replaceAll(key, value), template);
}

await mkdir(output, { recursive: true });
await mkdir(assets, { recursive: true });
await cp(path.join(root, "tools", "axioms-build", "node_modules", "katex", "dist", "fonts"), path.join(assets, "fonts"), { recursive: true });
await cp(path.join(root, "tools", "axioms-build", "node_modules", "katex", "dist", "katex.min.css"), path.join(assets, "katex.min.css"));
await cp(path.join(root, "tools", "axioms-build", "node_modules", "katex", "LICENSE"), path.join(assets, "LICENSE.txt"));
const pages = [];
for (const article of articles) {
  const markdown = (await readFile(path.join(source, article.file), "utf8")).replace(/\r\n/g, "\n");
  const title = markdown.match(/^# ([^\n]+)/m)?.[1];
  if (!title) throw new Error(article.file + " needs a Markdown title.");
  pages.push({ ...article, markdown, title });
}
for (const [index, article] of pages.entries()) {
  const html = articlePage(article, article.markdown, pages[index - 1], pages[index + 1]);
  await writeFile(path.join(output, article.url), html, "utf8");
  console.log("Built", path.join("writing", "axioms", article.url));
}
