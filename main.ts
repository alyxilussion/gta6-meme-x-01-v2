/**
 * Entrypoint: copy POST.json to the output directory.
 *
 * Stdlib only (the grader container installs nothing, and the program runs
 * with no network). The meme itself is rendered by draw_meme.py at build
 * time and committed as meme.png; this program just hands the post file
 * over, so both grader runs write identical bytes. It never touches the
 * network, the picture, or anything outside its own directory.
 */
import * as fs from "node:fs";
import * as path from "node:path";

function main(): number {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
  fs.mkdirSync(outDir, { recursive: true });
  const here = path.dirname(new URL(import.meta.url).pathname);
  const src = path.join(here, "POST.json");
  const dst = path.join(outDir, "POST.json");
  fs.copyFileSync(src, dst);
  const bytes = fs.statSync(dst).size;
  console.log(`wrote ${dst} (${bytes} bytes)`);
  return 0;
}

process.exit(main());
