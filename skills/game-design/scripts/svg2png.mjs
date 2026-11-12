// Render an SVG to PNG so edits can be inspected visually (open the PNG afterwards).
// Install once in your working directory (not globally): npm i --prefix ./.tools @resvg/resvg-js
// Usage: node svg2png.mjs <in.svg> <out.png> [width-px] [background, e.g. "#2B2730"]
// Any other SVG renderer (Inkscape, rsvg-convert, a browser) works just as well.
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join } from 'node:path';

const [input, output, width, background] = process.argv.slice(2);
if (!input || !output) {
  console.error('Usage: node svg2png.mjs <in.svg> <out.png> [width-px] [background]');
  process.exit(2);
}
let Resvg;
try {
  ({ Resvg } = createRequire(join(process.cwd(), '.tools', 'x.js'))('@resvg/resvg-js'));
} catch {
  console.error('Not installed. From your working directory run: npm i --prefix ./.tools @resvg/resvg-js');
  process.exit(1);
}
const options = { fitTo: width ? { mode: 'width', value: Number(width) } : { mode: 'original' } };
if (background) options.background = background;
const png = new Resvg(readFileSync(input), options).render().asPng();
writeFileSync(output, png);
console.log('saved', output, png.length, 'bytes');
