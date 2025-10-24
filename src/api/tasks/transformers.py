import logging
import pandas as pd
from bases.interfaces.transformers import TransformInterface

logger = logging.getLogger(__name__)


class YFinanceTransform(TransformInterface):
    
    def do_transform(self, **kwargs):
        """Transforma e enriquece os dados financeiros extraídos via yfinance."""
        df = kwargs.get('data')
        
        if df is None or df.empty:
            logger.warning("⚠️ Nenhum dado para transformar.")
            return pd.DataFrame()
        
        logger.info("⚙️ Iniciando transformação de %d registros do YFinance...", len(df))

        try:
            df = df.rename(columns=str.lower)
            df = df.dropna(subset=["close"])
            logger.debug("🧹 Registros após remoção de valores nulos: %d", len(df))
            df["pct_change"] = df["close"].pct_change().fillna(0)

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

            df["ma_7d"] = df["close"].rolling(window=7).mean().round(2)
            df["ma_30d"] = df["close"].rolling(window=30).mean().round(2)

            df = df.drop_duplicates(subset=["date"], keep="last")

            logger.info("✅ Transformação concluída com sucesso. %d registros finais.", len(df))
            logger.debug("📊 Colunas finais: %s", df.columns.tolist())

            return df

        except Exception as err:
            logger.exception("❌ Erro durante a transformação dos dados: %s", err)
            raise
