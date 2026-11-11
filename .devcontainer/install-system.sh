#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

task_sudo=()
if [[ $EUID -ne 0 ]]; then
  task_sudo=(sudo)
fi

missing_packages=()
while IFS= read -r package; do
  [[ -z "$package" || "$package" == \#* ]] && continue
  if [[ "$(dpkg-query -W -f='${Status}' "$package" 2>/dev/null || true)" != "install ok installed" ]]; then
    missing_packages+=("$package")
  fi
done < .devcontainer/system-packages.txt

if (( ${#missing_packages[@]} )); then
  "${task_sudo[@]}" apt-get update
  "${task_sudo[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${missing_packages[@]}"
fi

source .devcontainer/quarto-version.env
if ! command -v quarto >/dev/null || [[ "$(quarto --version)" != "$QUARTO_VERSION" ]]; then
  architecture="$(dpkg --print-architecture)"
  case "$architecture" in
    amd64) expected_sha="$QUARTO_SHA256_AMD64" ;;
    arm64) expected_sha="$QUARTO_SHA256_ARM64" ;;
    *) printf 'Arquitectura no compatible: %s\n' "$architecture" >&2; exit 1 ;;
  esac
  download_dir="$(mktemp -d /tmp/talleres-quarto.XXXXXX)"
  trap 'rm -rf "$download_dir"' EXIT
  installer="$download_dir/quarto.deb"
  curl --fail --location --retry 3 --connect-timeout 20 \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${architecture}.deb" \
    --output "$installer"
  printf '%s  %s\n' "$expected_sha" "$installer" | sha256sum --check
  "${task_sudo[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$installer"
fi

bash .devcontainer/install-tex.sh
