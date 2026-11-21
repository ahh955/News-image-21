// main.ts — make.fun bounty entry: news-image-20261121.
// Copies the pre-built entry.png (a 1024x1024 newspaper front page summing up
// the world news of Saturday 21 November 2026) to the output directory.
// Node 22, standard library only. No network access at runtime.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const DEST = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1024 * 1024; // 1 MiB

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

const buf = readFileSync(SRC);

if (buf.length > MAX_BYTES) {
  fail(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  fail("entry.png: missing or invalid PNG signature");
}

// First chunk must be IHDR: 4-byte length (13) at offset 8, chunk type "IHDR"
// at offset 12, then width/height as big-endian uint32 at offsets 16 and 20.
if (buf.readUInt32BE(8) !== 13 || buf.subarray(12, 16).toString("ascii") !== "IHDR") {
  fail("entry.png: first chunk is not a valid IHDR");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  fail(`entry.png is ${width}x${height}, larger than the 1024x1024 limit`);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DEST);
console.log(`wrote ${DEST} (${buf.length} bytes, ${width}x${height})`);
