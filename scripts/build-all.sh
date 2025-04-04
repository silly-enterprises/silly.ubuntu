#!/bin/bash
set -e
echo "[silly] Building all .deb packages..."
for pkg in packages/*; do
  name=$(basename "$pkg")
  version=$(grep Version "$pkg/DEBIAN/control" | awk '{print $2}')
  outdir="apt/pool/main/${name:0:1}/$name"
  mkdir -p "$outdir"
  echo "  → Building $name ($version)"

  # Ensure maintainer scripts are executable
  for f in preinst postinst prerm postrm; do
    [ -f "$pkg/DEBIAN/$f" ] && chmod 755 "$pkg/DEBIAN/$f"
  done

  fakeroot dpkg-deb --build "$pkg" "$outdir/${name}_${version}_all.deb"
done
echo "[silly] Done. Packages saved to apt/pool."
