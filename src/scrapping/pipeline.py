import logging
import time
from bases.interfaces.extractor import ExtractInterface
from bases.interfaces.loader import LoadInterface
from bases.interfaces.transformers import TransformInterface
from scrapping.tasks.extractor import ScrappingExtractor
from scrapping.tasks.transformer import ScrappingTransformer
from scrapping.tasks.loader import ScrappingLoader


logger = logging.getLogger(__name__)


class ScrappingPipeline:
    def __init__(
        self,
        extractor: ExtractInterface = None,
        transformer: TransformInterface = None,
        loader: LoadInterface = None,
    ):
        self.extractor = extractor or ScrappingExtractor()
        self.transformer = transformer or ScrappingTransformer()
        self.loader = loader or ScrappingLoader()

    def run(self, **kwargs):
        start_time = time.perf_counter()
        logger.info("🚀 Iniciando pipeline de Scraping...")

        try:
            # ETAPA 1: Extração
            logger.info("📡 Iniciando extração de dados...")
            data_extracted = self.extractor.do_extract(**kwargs)
            logger.info("✅ Extração concluída com sucesso (%d registros).", len(data_extracted))

            # ETAPA 2: Transformação
            logger.info("⚙️ Iniciando transformação de dados...")
            data_transformed = self.transformer.do_transform(
                data_extracted=data_extracted, **kwargs
            )
            logger.info("✅ Transformação concluída. %d registros processados.", len(data_transformed))

            # ETAPA 3: Carga
            logger.info("💾 Iniciando carga dos dados...")
            self.loader.do_load(data_transformed=data_transformed, **kwargs)
            logger.info("✅ Carga concluída com sucesso no destino final.")

            df_news = self.loader.get_news_as_dataframe()
            logger.debug("📊 Preview dos dados carregados:\n%s", df_news.head())

            elapsed = time.perf_counter() - start_time
            logger.info("🏁 Pipeline de Scraping finalizado em %.2fs", elapsed)

        except Exception as err:
            logger.exception("❌ Erro durante a execução do pipeline: %s", err)
            raise
