#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
source .devcontainer/texlive-version.env

task_sudo=()
if [[ $EUID -ne 0 ]]; then
  task_sudo=(sudo)
fi
case "$(dpkg --print-architecture)" in
  amd64) platform=x86_64; tex_arch=x86_64-linux; expected_sha="$TINYTEX_SHA256_AMD64" ;;
  arm64) platform=arm64; tex_arch=aarch64-linux; expected_sha="$TINYTEX_SHA256_ARM64" ;;
  *) printf 'Arquitectura de TeX Live no compatible.\n' >&2; exit 1 ;;
esac
tex_root="/opt/talleres-texlive/$TINYTEX_VERSION"
tex_bin="$tex_root/bin/$tex_arch"
run_tex() {
  "${task_sudo[@]}" env PATH="$tex_bin:$PATH" "$@"
}

if [[ ! -f "$tex_root/.talleres-ready" ]]; then
  archive="/tmp/TinyTeX-linux-$platform-v$TINYTEX_VERSION.tar.xz"
  if [[ ! -f "$archive" ]] || ! printf '%s  %s\n' "$expected_sha" "$archive" | sha256sum --check --status; then
    curl --fail --location --retry 3 --connect-timeout 20 \
      "https://github.com/rstudio/tinytex-releases/releases/download/v$TINYTEX_VERSION/TinyTeX-linux-$platform-v$TINYTEX_VERSION.tar.xz" \
      --output "$archive"
  fi
  printf '%s  %s\n' "$expected_sha" "$archive" | sha256sum --check
  "${task_sudo[@]}" mkdir -p "$tex_root"
  "${task_sudo[@]}" tar -xJf "$archive" --strip-components=1 -C "$tex_root"
  run_tex "$tex_bin/tlmgr" option repository https://tlnet.yihui.org
fi

if ! "$tex_bin/kpsewhich" spanish.ldf >/dev/null || \
   ! "$tex_bin/kpsewhich" listingsutf8.sty >/dev/null; then
  run_tex "$tex_bin/tlmgr" update --self
  run_tex "$tex_bin/tlmgr" install collection-langspanish listingsutf8
fi
"${task_sudo[@]}" touch "$tex_root/.talleres-ready"

# Los enlaces dan la misma versión a la terminal, Quarto y LaTeX Workshop.
run_tex "$tex_bin/tlmgr" option sys_bin /usr/local/bin
run_tex "$tex_bin/tlmgr" path add
version_output="$("$tex_bin/pdflatex" --version)"
if [[ "$version_output" != *"TeX Live $TEXLIVE_YEAR"* ]]; then
  printf 'La instalación no corresponde a TeX Live %s.\n' "$TEXLIVE_YEAR" >&2
  exit 1
fi
printf 'TeX Live %s instalado en %s\n' "$TEXLIVE_YEAR" "$tex_root"
