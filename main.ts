// news-image-20261121 v2 entrypoint (Node 22, standard library only).
//
// Copies the pre-built entry.png beside this file to the output directory:
// $MAKEFUN_OUTPUT_DIR when set (local runs), /output inside the grader.
// Before copying it checks the PNG signature, the 1 MiB size limit and the
// 1024x1024 dimension limit (read from the IHDR chunk), so a corrupt,
// oversized or over-dimensioned image fails loudly instead of entering the
// heat. No network access at runtime; both runs write the same bytes.
//
// Run it with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIMENSION = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

const buf = readFileSync(src);
if (!buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG file');
}
if (buf.length > MAX_BYTES) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}
// IHDR chunk: length (4) + "IHDR" (4) + width (4, BE) + height (4, BE).
if (buf.length < 24 || buf.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`wrote ${dest} (${buf.length} bytes)`);
