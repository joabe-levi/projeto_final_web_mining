import logging
from datetime import datetime
from bases.interfaces.transformers import TransformInterface

logger = logging.getLogger(__name__)


class ScrappingTransformer(TransformInterface):
    required_fields = [
        "tipo_noticia",
        "titulo_noticia",
        "url_noticia",
        "data_noticia",
    ]

    def do_transform(self, **kwargs):
        """Transforma e valida os dados extraídos das notícias."""
        data_extracted = kwargs.get("data_extracted", {})
        if not data_extracted:
            logger.warning("⚠️ Nenhum dado fornecido para transformação.")
            return {"data": [], "metadata": {"total_original": 0, "total_valid": 0}}

        news_list = data_extracted.get("data", [])
        data_extraction_time = data_extracted.get("data_extracao", "N/A")

        logger.info("⚙️ Iniciando transformação de %d notícias...", len(news_list))

        valid_news = []
        invalid_count = 0

        for i, news in enumerate(news_list):
            if self.is_valid(news):
                valid_news.append(news)
            else:
                invalid_count += 1
                logger.debug(
                    "🪶 Notícia %d filtrada - campos obrigatórios faltando (%s)",
                    i + 1,
                    [f for f in self.required_fields if not news.get(f)],
                )

        logger.info(
            "✅ Transformação concluída: %d válidas | %d filtradas", len(valid_news), invalid_count
        )

        metadata = {
            "total_original": len(news_list),
            "total_valid": len(valid_news),
            "total_filtered": invalid_count,
            "data_extracao": data_extraction_time,
            "data_transformacao": self._get_current_timestamp(),
        }

        logger.debug("📊 Metadados de transformação: %s", metadata)

        return {"data": valid_news, "metadata": metadata}

    def is_valid(self, news_item):
        if not isinstance(news_item, dict):
            logger.debug("❌ Item inválido: tipo incorreto (%s)", type(news_item))
            return False

        for field in self.required_fields:
            value = news_item.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                return False

        return True

    def _get_current_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
