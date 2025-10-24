import logging, time

from api.tasks.extractor import YFinanceExtract
from api.tasks.loader import YFinanceLoad
from api.tasks.transformers import YFinanceTransform
from bases.interfaces.pipeline import PipelineInterface

logger = logging.getLogger(__name__)


class YFinancePipeline(PipelineInterface):
    
    def __init__(self, **kwargs):
        self.extractor = kwargs.get('extractor', YFinanceExtract())
        self.transformer = kwargs.get('transformer', YFinanceTransform())
        self.loader = kwargs.get('loader', YFinanceLoad())

    def run(self):
        start_time = time.perf_counter()
        logger.info("🚀 Iniciando pipeline de ETL para YFinance...")

        try:
            # 1️⃣ Extração
            logger.info("📡 Iniciando extração de dados da API YFinance...")
            data = self.extractor.do_extract()
            logger.info("✅ Extração concluída com sucesso (%d registros).", len(data))

            # 2️⃣ Transformação
            logger.info("⚙️ Iniciando transformação dos dados extraídos...")
            transformed_data = self.transformer.do_transform(df=data)
            logger.info("✅ Transformação concluída. %d registros processados.", len(transformed_data))

            # 3️⃣ Carga
            logger.info("💾 Iniciando carga dos dados no banco DuckDB...")
            self.loader.do_load(df=transformed_data)
            logger.info("✅ Carga concluída com sucesso no banco '%s'.", self.loader.db_path)

            duration = time.perf_counter() - start_time
            logger.info("🏁 Pipeline YFinance finalizado em %.2fs", duration)

        except Exception as e:
            logger.exception("❌ Falha durante a execução do pipeline YFinance: %s", e)
            raise
