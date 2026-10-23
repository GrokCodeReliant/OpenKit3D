#!/bin/bash
# Renders every SVG deliverable to PNG with headless Chrome (no installs). Run from art/styleframe.
set -e; cd "$(dirname "$0")"; A=$(cd ..; pwd)
R(){ google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --default-background-color=00000000 --user-data-dir=/tmp/chr$RANDOM --window-size=$3 --screenshot=$2 file://$1 >/dev/null 2>&1; }
dim(){ python3 -c "import re,sys;t=open(sys.argv[1]).read(800);print(re.search(r'width=\"(\d+)\"',t).group(1)+','+re.search(r'height=\"(\d+)\"',t).group(1))" $1; }
rm -f $A/atlas/*_parts@2x.png $A/batch[123]/*.png $A/backgrounds/*.png *.png
for f in $A/atlas/*.svg $A/batch[123]/contact_sheet.svg $A/backgrounds/*.svg; do R $f ${f%.svg}.png $(dim $f); done
R $A/batch1/composite_scene.svg $A/batch1/composite_scene_1080.png 1080,1920
for f in street bag_ui; do R $PWD/styleframe_$f.svg $PWD/styleframe_$f.png 1080,1920; done
python3 -c "
from PIL import Image
for a,b in [('$A/batch1/composite_scene_1080.png','$A/batch1/composite_scene_360.png'),('styleframe_street.png','styleframe_street_360.png'),('styleframe_bag_ui.png','styleframe_bag_ui_360.png')]: Image.open(a).resize((360,640),Image.LANCZOS).save(b)"
