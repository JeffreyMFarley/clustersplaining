#!/bin/sh

rm -rf ./cel/*.html
python3 display_swatches.py
python3 build_clusters.py
python3 build_clusters.py --use-hsl
python3 build_clusters.py --use-hsl -k 64
python3 build_clusters.py --use-hsl -n
python3 build_clusters.py --use-hsl -n -k 64
python3 build_clusters.py --use-hsl -n --trial A
python3 build_clusters.py --use-hsl -n --trial B
python3 build_clusters.py --use-hsl -n --trial C
python3 build_clusters.py --use-hsl -n --trial D
python3 build_clusters.py --use-hsl -n --trial E
