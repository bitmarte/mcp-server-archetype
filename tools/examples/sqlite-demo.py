from typing import Optional
from mcp_core.core import core_api

# Nel .env ci sarà qualcosa del tipo: SQLITE_DB_URL_SQLITE-DEMO="file:/app/data/home-assistant_v2.db?mode=ro&immutable=1"
ALIAS_DEMO_DB = "sqlite-demo"

# ============================================
# Funzione di utilità per limite sicuro
# ============================================
def get_limit(default: int, max_allowed: int = 1000, user_limit: Optional[int] = None) -> int:
    """
    Restituisce un limite sicuro per query SQL, evitando di superare soglie massime.
    
    Parameters:
        default (int): valore di default se user_limit non è specificato
        max_allowed (int): massimo valore consentito
        user_limit (Optional[int]): valore richiesto dall'utente
    
    Returns:
        int: limite finale sicuro da usare nelle query
    """
    if user_limit is None:
        return default
    return min(user_limit, max_allowed)

# ============================================
# Demo: valori unici di una colonna
# ============================================
@core_api.mcp.tool
def get_unique_column_values(table_name: str, column_name: str, limit: Optional[int] = None) -> list[dict]:
    """
    Restituisce i valori distinti di una colonna in una tabella SQLite demo.
    
    L’LLM può usare questa funzione per:
      - conoscere quali valori esistono in una colonna
      - costruire query più mirate basate sui valori disponibili
      - generare report di esempio o aggregazioni
    
    Parameters:
        table_name (str): nome della tabella su cui effettuare la query
        column_name (str): nome della colonna di cui ottenere valori distinti
        limit (Optional[int]): numero massimo di record da restituire
    
    Returns:
        list[dict]: lista di record, ciascuno un dizionario {column_name: valore}.
                     In caso di errore, restituisce [{"error": "messaggio"}]
    """
    sqlite_helper = core_api.sqlite
    logger = core_api.logger
    safe_limit = get_limit(default=100, max_allowed=1000, user_limit=limit)
    
    sql = f'SELECT DISTINCT "{column_name}" FROM "{table_name}" LIMIT {safe_limit}'
    
    try:
        rows = sqlite_helper.query(sql=sql, alias=ALIAS_DEMO_DB)
        records = [dict(row) for row in rows]
        logger.info(f"get_unique_column_values: {len(records)} record restituiti per colonna '{column_name}' in '{table_name}'")
        return records
    except Exception as e:
        logger.error(f"Errore get_unique_column_values: {e}")
        return [{"error": str(e)}]

# ============================================
# Demo: aggregazione semplice
# ============================================
@core_api.mcp.tool
def aggregate_column_sum(table_name: str, column_name: str, group_by_column: Optional[str] = None) -> dict:
    """
    Restituisce la somma dei valori numerici di una colonna,
    opzionalmente raggruppata per un’altra colonna.
    
    L’LLM può usare questa funzione per:
      - capire i totali aggregati di una colonna numerica
      - eseguire analisi semplici sui dati demo
      - generare statistiche di esempio o report
    
    Parameters:
        table_name (str): nome della tabella su cui effettuare la query
        column_name (str): colonna numerica di cui calcolare la somma
        group_by_column (Optional[str]): colonna opzionale per raggruppamento
    
    Returns:
        dict: oggetto con chiavi:
            - "records": lista di dizionari {"group_key": valore, "total": somma}
            - "error": messaggio di errore, None se tutto ok
    """
    sqlite_helper = core_api.sqlite
    logger = core_api.logger

    try:
        if group_by_column:
            sql = f"""
            SELECT "{group_by_column}" AS group_key, SUM("{column_name}") AS total
            FROM "{table_name}"
            GROUP BY "{group_by_column}"
            """
        else:
            sql = f'SELECT SUM("{column_name}") AS total FROM "{table_name}"'

        rows = sqlite_helper.query(sql=sql, alias=ALIAS_DEMO_DB)
        records = [dict(row) for row in rows]
        logger.info(f"aggregate_column_sum: {len(records)} record restituiti")
        return {"records": records, "error": None}
    except Exception as e:
        logger.error(f"Errore aggregate_column_sum: {e}")
        return {"records": [], "error": str(e)}
