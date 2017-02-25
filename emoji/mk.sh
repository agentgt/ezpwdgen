#!/usr/bin/env bash
# curl http://unicode.org/emoji/charts/emoji-annotations.html
# v4.0
cat emoji.html | grep -o "<a href='#[^']*'" \
| sed -E "s/.*#([^']+).*/\1/" \
| grep "^[a-z][a-z][a-z][a-z]*$" \
| sort \
| uniq
