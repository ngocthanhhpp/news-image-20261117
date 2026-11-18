# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)

One image that sums up the world news of Tuesday 17 November 2026: a dated front page led by the tanker attacks in the Strait of Hormuz, with Ukraine's record drone strike, Trump in Manila and the Quad minerals deals, Nvidia's earnings, Israel's election-interference claims, the EU's Rwanda return hub, and more.

`main.ts` copies `entry.png` to `/output/entry.png` (no network, same bytes every run). `tools/draw.py` draws the image with Pillow.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
