import logging
from bases.interfaces.extractor import ExtractInterface
from scrapping.crawlers.infomoney import InfoMoneyCrawler

logger = logging.getLogger(__name__)


class ScrappingExtractor(ExtractInterface):
    def __init__(self, crawler: InfoMoneyCrawler = None, **kwargs):
        super().__init__(**kwargs)
        self.crawler = crawler or InfoMoneyCrawler(**kwargs)

    def do_extract(self, **kwargs):
        """Extrai dados usando o crawler com gerenciamento automático de recursos."""
        logger.info("📡 Iniciando extração de dados com InfoMoneyCrawler...")

        try:
            with self.crawler as crawler:
                raw_content = crawler.run()

            # Validação básica do retorno
            if not raw_content:
                logger.warning("⚠️ Nenhum conteúdo retornado pelo crawler.")
            else:
                logger.info("✅ Extração concluída com sucesso. %d registros encontrados.", len(raw_content))

            return raw_content

        except Exception as err:
            logger.exception("❌ Erro durante a extração de dados: %s", err)
            raise
