import logging
import yfinance as yf

from datetime import datetime, timedelta

from bases.interfaces.extractor import ExtractInterface

logger = logging.getLogger(__name__)


class YFinanceExtract(ExtractInterface):
    
    def __init__(self, **kwargs):
        self.symbol = kwargs.get('symbol', 'BTC-USD')
        self.interval = kwargs.get('interval', '1d')
        super().__init__(**kwargs)
    
    def do_extract(self):
        start_time = datetime.now()
        logger.info("📡 Iniciando extração de dados para %s (%s)...", self.symbol, self.interval)

        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=180)  # ~6 meses
            logger.debug("🔍 Período solicitado: %s → %s", start_date.date(), end_date.date())

            df = yf.download(
                self.symbol,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                interval=self.interval,
                multi_level_index=False
            )

            if df.empty:
                logger.warning("⚠️ Nenhum dado foi retornado pela API do yfinance (%s).", self.symbol)
                return df

            logger.info("✅ Extração concluída com sucesso. %d registros obtidos.", len(df))
            logger.debug("📊 Colunas retornadas: %s", list(df.columns))

            df.reset_index(inplace=True)
            return df

        except Exception as err:
            logger.exception("❌ Erro durante a extração de dados do yfinance: %s", err)
            raise

        finally:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info("⏱️ Tempo total de extração: %.2fs", elapsed)
