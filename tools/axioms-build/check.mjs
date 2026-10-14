import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const directory = path.join(root, "writing", "axioms");
const sequence = ["0", "1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "2-1", "2-2", "2-3", "2-4", "2-5"];
const index = await readFile(path.join(directory, "index.html"), "utf8");

for (const [position, name] of sequence.entries()) {
  const html = await readFile(path.join(directory, name + ".html"), "utf8");
  const sourceName = name === "0" ? "00-introduction" : name;
  const source = await readFile(path.join(root, "公理：数学史与哲学", "英文版本", sourceName + ".md"), "utf8");
  const navigation = html.match(/<nav class="site-nav"[\s\S]*?<\/nav>/)?.[0] || "";
  const pagination = html.match(/<nav class="reader-pagination"[\s\S]*?<\/nav>/)?.[0] || "";
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, name + ": duplicate IDs");
  assert.equal((navigation.match(/<a /g) || []).length, 4, name + ": global navigation");
  assert(!navigation.includes("#thinking") && !navigation.includes("#beyond"));
  for (const match of html.matchAll(/href="#([^"]+)"/g)) {
    assert(ids.includes(match[1]), name + ": missing anchor " + match[1]);
  }
  assert(index.includes('href="' + name + '.html"'), name + ": absent from index");
  assert(!html.includes("katex-error") && !html.includes("@@"), name + ": render failure");
  if (position > 0) {
    assert(pagination.includes('href="' + sequence[position - 1] + '.html"'), name + ": previous");
  }
  if (position + 1 < sequence.length) {
    assert(pagination.includes('href="' + sequence[position + 1] + '.html"'), name + ": next");
  } else {
    assert(!pagination.includes("<small>Next</small>"), name + ": unpublished next article");
  }
  const continued = html.match(/class="reader-continuation"/g) || [];
  assert.equal(continued.length, name === "2-5" ? 1 : 0);
  if (name === "2-5") {
    const header = html.match(/<header class="reader-article-header">[\s\S]*?<\/header>/)[0];
    assert(header.indexOf("reader-continuation") > header.indexOf("reader-deck"));
    assert(source.includes("**To be continued**"));
  }
  if (name.startsWith("2-")) {
    assert((html.match(/class="toc-children"/g) || []).length > 0, name + ": second-level contents");
    const tables = (html.match(/<table>/g) || []).length;
    assert.equal(tables, (html.match(/class="reader-table"/g) || []).length, name + ": unwrapped table");
    const prose = html.match(/<div class="reader-prose">([\s\S]*?)<\/div>\s*<nav class="reader-pagination"/)?.[1] || "";
    assert(!prose.includes("$$"), name + ": unrendered math delimiter");
  }
  console.log(name + ": passed");
}

function simulate(table) {
  const tape = new Map();
  let head = 0, state = "A", steps = 0;
  while (state !== "H" && steps < 10000) {
    const [write, direction, next] = table[state][tape.get(head) || 0];
    tape.set(head, Number(write));
    head += direction === "R" ? 1 : -1;
    state = next;
    steps++;
  }
  return { steps, ones: [...tape.values()].filter(Boolean).length, state };
}
assert.deepEqual(
  simulate({ A: ["1RB", "1LB"], B: ["1LA", "0LC"], C: ["1RH", "1LD"], D: ["1RD", "0RA"] }),
  { steps: 107, ones: 13, state: "H" },
);
assert.deepEqual(
  simulate({ A: ["1RB", "1LB"], B: ["1LA", "1RH"] }),
  { steps: 6, ones: 4, state: "H" },
);
console.log("Both published Turing-machine tables reproduce the stated runs.");
