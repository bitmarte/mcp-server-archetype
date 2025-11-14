#!/usr/bin/env bash
set -e

# Usa il nome del folder come IMAGE_NAME se non specificato
IMAGE_NAME="${IMAGE_NAME:-$(basename "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")}"
TAG="${TAG:-latest}"

# creo il folder localmente per essere eventualmente pronto alla dipendenza da locale del core e non far rompere poi il Containerfile
mkdir -p vendor

MCP_HASH=""

# Se viene passato l'argomento "local-mcpcore", copia mcp-core nella cartella vendor/
if [[ "$1" == "--local-mcpcore" ]]; then
    echo "=== Modalità sviluppo locale: includo mcp-core dal percorso ../mcp-core ==="
    rm -rf vendor/mcp-core
    cp -r ../mcp-core vendor/mcp-core
else
    echo "=== Modalità standard: userò mcp-core da repository remoto ==="
    rm -rf vendor/mcp-core 2> /dev/null
    if [[ "$1" == "--force-remote-mcpcore-update" ]]; then
        echo "Richiesta forzatura aggiornamento remoto..."
        truncate -s 0 > .mcp-core_remote_tag
    fi
    # Recupero hash dell'ultimo commit del branch main
    MCP_HASH=$(git ls-remote https://github.com/bitmarte/mcp-core.git HEAD | cut -f1)
    echo "Ultimo commit mcp-core: $MCP_HASH"
    # Scrivo l'hash in un file che Docker copierà
    echo $MCP_HASH > .mcp-core_remote_tag
fi

echo "=== Build container ${IMAGE_NAME}:${TAG} ==="
podman build \
    --build-arg MCP_CORE_LAST_COMMIT=${MCP_HASH:-main} \
    -t "${IMAGE_NAME}:${TAG}" .

echo "=== Build completata con successo ==="
