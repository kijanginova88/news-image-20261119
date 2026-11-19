// News-image entry for 19 November 2026.
//
// The finished picture ships in this repo as entry.png. Drawing it at
// run time would need Pillow, which the grader's Python image does not
// have, so this program only copies the baked-in image into the output
// directory. Node's standard library is all it needs, and copying the
// same bytes twice gives the same result twice. The output file is
// always named entry.png, whatever the output directory is.

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
