#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
action="${1:-status}"
case "$action" in
  status) git submodule status -- documents_overleaf; exit 0 ;;
  check|init|pull) ;;
  *) printf 'Uso: bash scripts/overleaf.sh [status|check|init|pull]\n' >&2; exit 2 ;;
esac

OVERLEAF_GIT_TOKEN="${OVERLEAF_GIT_TOKEN:-${OVERLEAF_TOKEN:-${OVERLEAF:-}}}"
if [[ -z "$OVERLEAF_GIT_TOKEN" ]]; then
  if [[ ! -t 0 ]]; then
    printf 'El secret OVERLEAF aún no está disponible en esta sesión.\n' >&2
    printf 'Si acabas de crearlo, detén y vuelve a abrir el Codespace para cargarlo.\n' >&2
    exit 1
  fi
  printf 'Obtén el token en Overleaf > Account Settings > Git Integration.\n'
  read -r -s -p 'Token de Git de Overleaf (no se mostrará ni guardará): ' OVERLEAF_GIT_TOKEN
  printf '\n'
  if [[ -z "$OVERLEAF_GIT_TOKEN" ]]; then
    printf 'No se introdujo un token.\n' >&2
    exit 1
  fi
fi
export OVERLEAF_GIT_TOKEN
askpass_dir="$(mktemp -d /tmp/talleres-overleaf.XXXXXX)"
trap 'unset OVERLEAF_GIT_TOKEN; rm -rf "$askpass_dir"' EXIT
cat > "$askpass_dir/askpass.sh" <<'ASKPASS'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf '%s\n' git ;;
  *Password*) printf '%s\n' "$OVERLEAF_GIT_TOKEN" ;;
  *) exit 1 ;;
esac
ASKPASS
chmod 700 "$askpass_dir/askpass.sh"
export GIT_ASKPASS="$askpass_dir/askpass.sh"
export GIT_TERMINAL_PROMPT=0
export LC_ALL=C

report_revision() {
  local latest="$1"
  if [[ -f documents_overleaf/.git ]]; then
    local current
    current="$(git -C documents_overleaf rev-parse HEAD)"
    printf 'Revisión de la copia local: %s.\n' "${current:0:12}"
    if [[ "$current" != "$latest" ]]; then
      printf 'AVISO: la copia local difiere de Overleaf (%s).\n' "${latest:0:12}"
      printf 'Para traer sus archivos actuales: bash scripts/overleaf.sh pull\n'
    fi
  else
    printf 'Los documentos todavía no están descargados. Usa bash scripts/overleaf.sh init.\n'
  fi
}

if [[ "$action" == check ]]; then
  url="$(git config -f .gitmodules --get submodule.documents_overleaf.url)"
  git -c credential.helper= ls-remote "$url" HEAD > "$askpass_dir/remote-head"
  read -r remote_head _ < "$askpass_dir/remote-head"
  printf 'Conexión autenticada con Overleaf: OK (HEAD %s).\n' "${remote_head:0:12}"
  report_revision "$remote_head"
elif [[ "$action" == init ]]; then
  git -c credential.helper= submodule update --init --checkout -- documents_overleaf
else
  # Actualiza el puntero local. Revisar y guardar ese cambio en GitHub es otro paso.
  git -c credential.helper= submodule update --init --remote --checkout -- documents_overleaf
fi

if [[ "$action" != check ]]; then
  # El .gitignore del repositorio principal no se aplica dentro del submódulo.
  if ! git -C documents_overleaf check-ignore -q build/; then
    exclude_path="$(git -C documents_overleaf rev-parse --git-path info/exclude)"
    printf '\n# Compilación local de LaTeX\n/build/\n' >> "$exclude_path"
  fi
  report_revision "$(git -C documents_overleaf rev-parse origin/HEAD)"
fi
