# MCP Server Archetype

**MCP Server Archetype** è un template base per creare nuovi MCP Server figli utilizzando [Copier](https://copier.readthedocs.io/).  
Include la struttura minima necessaria per avviare un server MCP modulare con FastMCP, caricare tools e gestire configurazioni, container e script di avvio.

## Pre-requisiti

Per partire con mcp-server-archetype, i requisiti minimi sono:

- `Python 3.11+` → necessario per eseguire il codice MCP Core e FastMCP.
- `Podman` → per buildare e avviare il container.
- `Copier` → per generare server figli dal template.
- `pip` → per installare le dipendenze Python.

## Struttura del template

```
./
├── .env.jinja
├── .gitignore
├── Containerfile.jinja
├── build.sh.jinja
├── copier.yaml
├── readme.md
├── requirements.txt
├── start.sh.jinja
├── stop.sh.jinja
└── tools/
    └── default/
        └── health_check.py
```

## Funzionamento

Questo template è pensato per:

1. Fornire una base pronta all’uso per tutti i server MCP figli.
2. Gestire la configurazione tramite `.env`.
3. Caricare dinamicamente i tools Python.
4. Consentire la creazione di container personalizzati tramite template Jinja (`Containerfile.jinja`, `build.sh.jinja`).

### Tools

- La cartella `tools/` contiene già un tool di esempio `health_check.py`.
- I nuovi tools possono essere aggiunti nelle sottocartelle di `tools/`.
- Tutti i tools devono usare l’istanza globale `core_api` e il decoratore `@core_api.mcp.tool`.

Esempio:

```python
# tools/default/health_check.py
from mcp_core.core import core_api

@core_api.mcp.tool
def health_check() -> dict:
    core_api.logger.info("Eseguo health_check")
    return {"status": "ok"}
```

### Configurazione con Copier

Il file `copier.yaml` definisce:

- Nome e descrizione del progetto generato.
- Variabili interattive per personalizzare il server (porta, nome, path, ecc.).
- Template per file .env, Containerfile e script di avvio.

Esempio di comando per creare un nuovo server prendendo il core da Github:

```
copier copy gh:bitmarte/mcp-server-archetype my-new-mcp-server
```

Esempio di comando per creare un nuovo server prendendo il core da locale (repo clonato):

```
copier copy ./mcp-server-archetype my-new-mcp-server
```

### Avvio del server

Dopo aver generato il server figlio:

- Configura l’ambiente .env.
- Costruisci il container: `./build.sh`
- Avvia il server in container: `./start.sh`
- Ferma il container (se avviato con detached=true): `./stop.sh`

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