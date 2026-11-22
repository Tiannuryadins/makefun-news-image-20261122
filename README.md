# The World in One Image — 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/tiannuryadins/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/tiannuryadins/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for [news-image-20261122](https://make.fun/bounty/news-image-20261122):
"Sum up 22 November's world news in one image".

`main.py` (Python 3.13, standard library only) copies the sibling
`poster.png` — a 1024×1024 newspaper front page rendered at build time
by `render_poster.py` from verified 22 November 2026 news — to
`/output/entry.png` (two runs produce identical bytes; no network at
runtime).

Lead story: Iran strikes Bahrain — a missile-and-drone attack hit a
civilian industrial site; air defences intercepted the rest, no
casualties; the IRGC says US bases were the target.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
