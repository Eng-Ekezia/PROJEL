import logging
from fastapi import APIRouter

# --- CONFIGURAÇÃO DE LOGS ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PROJEL_DEBUG")

logger.info("==================================================")
logger.info(">>> INICIANDO CARREGAMENTO DE ROTAS (API.PY) <<<")
logger.info("==================================================")

api_router = APIRouter()

# 1. Tentar importar SYSTEM
try:
    from backend.api.v1.endpoints import system
    logger.info("✅ Módulo 'system' importado com sucesso.")
    api_router.include_router(system.router, prefix="/system", tags=["system"])
    logger.info("✅ Rota '/system' registrada.")
except Exception as e:
    logger.error(f"❌ FALHA CRÍTICA ao carregar 'system': {e}")

# 2. Tentar importar ZONAS
try:
    logger.info("--- Tentando importar Zonas ---")
    from backend.api.v1.endpoints import zonas
    logger.info("✅ Módulo 'zonas' importado.")
    
    if hasattr(zonas, 'router'):
        api_router.include_router(zonas.router, prefix="/zonas", tags=["zonas - influencias"])
        logger.info("✅ Rota '/zonas' registrada com sucesso.")
    else:
        logger.error("❌ O módulo 'zonas' foi importado, mas NÃO possui o objeto 'router' definido.")

except ImportError as ie:
    logger.error(f"❌ Erro de Importação em 'zonas': {ie}")
    logger.error("DICA: Verifique se o arquivo backend/api/v1/endpoints/zonas.py existe mesmo.")
except Exception as e:
    logger.error(f"❌ Erro Genérico em 'zonas': {e}")

# 3. Tentar importar LOCAIS
try:
    logger.info("--- Tentando importar Locais ---")
    from backend.api.v1.endpoints import locais
    logger.info("✅ Módulo 'locais' importado.")

    if hasattr(locais, 'router'):
        api_router.include_router(locais.router, prefix="/locais", tags=["locais - arquitetura"])
        logger.info("✅ Rota '/locais' registrada com sucesso.")
    else:
        logger.error("❌ O módulo 'locais' foi importado, mas NÃO possui o objeto 'router' definido.")

except ImportError as ie:
    logger.error(f"❌ Erro de Importação em 'locais': {ie}")
    logger.error("DICA: Verifique se o arquivo backend/api/v1/endpoints/locais.py existe mesmo.")
except Exception as e:
    logger.error(f"❌ Erro Genérico em 'locais': {e}")

logger.info("==================================================")
logger.info(">>> FIM DO CARREGAMENTO (API.PY) <<<")
logger.info("==================================================")