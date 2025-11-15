#!/bin/bash
# download_only_icons.sh

set -e

OUTDIR="icons_raw"
mkdir -p $OUTDIR

echo "Downloading Bootstrap Icons..."
wget -q https://github.com/twbs/icons/archive/refs/heads/main.zip -O bootstrap.zip
unzip -q bootstrap.zip "icons-main/icons/*" -d tmp_bootstrap
mv tmp_bootstrap/icons-main/icons/* $OUTDIR/
rm -rf tmp_bootstrap bootstrap.zip

echo "Downloading Feather Icons..."
wget -q https://github.com/feathericons/feather/archive/refs/heads/master.zip -O feather.zip
unzip -q feather.zip "feather-master/icons/*" -d tmp_feather
mv tmp_feather/feather-master/icons/* $OUTDIR/
rm -rf tmp_feather feather.zip

echo "Downloading Heroicons..."
wget -q https://github.com/tailwindlabs/heroicons/archive/refs/heads/master.zip -O heroicons.zip
unzip -q heroicons.zip "heroicons-master/optimized/*" -d tmp_heroicons
# Copy all optimized icons (outline/solid)
find tmp_heroicons/heroicons-master/optimized -type f -name "*.svg" -exec mv {} $OUTDIR/ \;
rm -rf tmp_heroicons heroicons.zip

echo "Downloading FontAwesome Free Icons..."
wget -q https://github.com/FortAwesome/Font-Awesome/archive/refs/heads/6.x.zip -O fa.zip
unzip -q fa.zip "Font-Awesome-6.x/svgs/*" -d tmp_fa
find tmp_fa/Font-Awesome-6.x/svgs -type f -name "*.svg" -exec mv {} $OUTDIR/ \;
rm -rf tmp_fa fa.zip

echo "Done. Icons saved to $OUTDIR/"