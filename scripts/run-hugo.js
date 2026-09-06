// Keep local, CI, and preview builds on the same Hugo Extended release.
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const root = path.resolve(__dirname, "..");
const version = fs.readFileSync(path.join(root, ".hugo-version"), "utf8").trim();
const binary = process.env.HUGO_BINARY || "hugo";
const probe = spawnSync(binary, ["version"], { encoding: "utf8", cwd: root });
if (probe.error || probe.status !== 0) {
  console.error(`Hugo ${version} Extended is required. Install it or set HUGO_BINARY to its executable.`);
  if (probe.error) console.error(probe.error.message);
  process.exit(1);
}
const actualVersion = probe.stdout.match(/\bhugo v([0-9]+\.[0-9]+\.[0-9]+)(?:[-+\s]|$)/)?.[1];
if (actualVersion !== version || !probe.stdout.includes("+extended")) {
  console.error(`Expected Hugo ${version} Extended; received: ${probe.stdout.trim()}`);
  console.error("Set HUGO_BINARY to a matching executable to avoid changing your global Hugo installation.");
  process.exit(1);
}

const result = spawnSync(binary, process.argv.slice(2), { cwd: root, stdio: "inherit" });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
