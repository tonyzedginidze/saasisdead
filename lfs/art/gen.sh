#!/bin/bash
slug="$1"; scene="$2"; R=/private/tmp/claude-501/-Volumes-external-nightcity/c6ff8367-4de4-47ae-8178-db9c43d8435c/scratchpad/ref
case $slug in hero|contribute|footer) p="$scene";; *) p="A wide short category banner scene, all content in a short wide horizontal strip across the middle with plain white above and below, a soft lilac-tinted ground band with grass tufts and a couple of small decor props. $scene";; esac
[ -f raw/$slug.png ] && exit 0
/Users/alvin/.claude/skills/nightcity-chatgpt-imagegen-oauth/chatgpt-imagegen-oauth "$p" --prompt-file style.md -i $R/reaper-canonical.png -i $R/scene-graveyard.png --size 1536x1024 --format png -o raw/$slug.png --quiet || echo "FAIL $slug"
