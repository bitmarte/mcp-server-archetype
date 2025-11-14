# MCP Server Archetype

**MCP Server Archetype** è un template base per creare nuovi MCP Server figli utilizzando [Copier](https://copier.readthedocs.io/).  
Include la struttura minima necessaria per avviare un server MCP modulare con FastMCP, caricare tools e gestire configurazioni, container e script di build/start/stop.

## Pre-requisiti

Per partire con mcp-server-archetype, i requisiti minimi sono:

- `Podman` → per buildare e avviare il container.
- `Copier` → per generare server figli dal template.

## Funzionamento

Questo template è pensato per:

1. Fornire una base pronta all’uso per tutti i server MCP figli.
2. Gestire la configurazione tramite `.env`.
3. Caricare dinamicamente i tools Python.

### Tools

- La cartella `tools/default` contiene già i tools di default del protocollo es.(`health_check.py`) con una implementazione fake.
- La cartella `tools/examples` contiene dei tools di esempio che però non vengono caricati dal server mcp; sono solo esempi da consultare.

Esempio di un tools:

```python
from mcp_core.core import core_api

@core_api.mcp.tool
def health_check() -> dict:
    core_api.logger.info("Eseguo health_check")
    return {"status": "ok"}
```

### Avvio del server

Dopo aver generato il server figlio:

- Configura l’ambiente .env.
- Costruisci il container: `./build.sh`
- Avvia il server in container: `./start.sh`
- Ferma il container (se avviato con detached=true): `./stop.sh`

#### Build

La build può essere lanciata nei seguenti modi:
- `./build.sh --local-mcpcore` → presuppone di avere il repo `mcp-core` a livello fratello dell'archetipo e usarà lui come modulo mcp-core, utile per lo sviluppo locale del core stesso
- `./build.sh` → scarica `mcp-core` dal repo github come dipendenza e ne congela la versione remota per le future build
- `./build.sh --force-remote-mcpcore-update` → scarica `mcp-core` dal repo github come dipendenza ignorando la versione precedentemente scaricata e ne congela la nuova versione remota per le future build

#### Start
Lo start può essere invocato nei seguenti modi:
- `./start.sh` → avvia il server restando appeso per la consultazione live dei log
- `./start.sh --detached` → avvia il server in modalità detached e quindi occorrerà lanciare `./stop.sh` per fermarlo

### Template Jinja

- `.env.jinja` → template del file .env con variabili configurabili.
- `Containerfile.jinja` → template per costruire l’immagine container.
- `build.sh.jinja` → script di build dell’immagine basato sul Containerfile.
- `start.sh.jinja / stop.sh.jinja` → script per avvio e stop del container.

Le variabili Jinja verranno sostituite da Copier con i valori specifici del server generato.

## Contributi

Per aggiungere nuovi strumenti o personalizzare il server:

- Creare/modificare tools nella cartella tools/.
- Aggiornare il .env.jinja se servono nuove variabili di configurazione.
- Modificare eventuali template Jinja se cambiano percorsi, porte o dipendenze.

## Note

- Questo template serve come base modulare: tutti i server figli creati avranno la stessa struttura coerente.
- I tools caricati automaticamente semplificano l’estendibilità del server.
- Utilizzando Copier, è possibile generare più server con configurazioni diverse mantenendo la stessa base di codice.