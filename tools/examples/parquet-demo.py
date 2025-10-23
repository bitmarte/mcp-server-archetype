from typing import Optional
from mcp_core.core import core_api

# ============================================
# Alias generico dei file Parquet
# ============================================
# Nel file .env es: PARQUET_FILES_ROOT_DEMO=/app/data/
ALIAS_DEMO = "demo"

# ============================================
# Funzione di utilità per limite sicuro
# ============================================
def get_limit(default: int, max_allowed: int = 1000, user_limit: Optional[int] = None) -> int:
    """
    Restituisce un limite sicuro per query SQL, evitando di superare soglie massime.
    """
    if user_limit is None:
        return default
    return min(user_limit, max_allowed)

# ============================================
# Funzione demo: elenco valori unici di una colonna
# ============================================
@core_api.mcp.tool
def get_unique_column_values(column_name: str, limit: Optional[int] = None) -> list[dict]:
    """
    Restituisce i valori unici di una colonna presente nel parquet demo.

    Parameters:
        column_name (str): nome della colonna da estrarre
        limit (int, optional): numero massimo di record da restituire

    Returns:
        list[dict]: lista di record {colonna: valore}
    """
    parquet_helper = core_api.parquet
    logger = core_api.logger
    safe_limit = get_limit(default=100, max_allowed=1000, user_limit=limit)
    
    sql = f'SELECT DISTINCT "{column_name}" FROM read_parquet("{ALIAS_DEMO}") LIMIT {safe_limit}'
    
    try:
        df = parquet_helper.query(sql=sql, alias=ALIAS_DEMO)
        records = df.to_dict(orient="records")
        logger.info(f"get_unique_column_values: restituiti {len(records)} record per colonna '{column_name}'")
        return records
    except Exception as e:
        logger.error(f"Errore get_unique_column_values: {e}")
        return [{"error": str(e)}]