import os, duckdb, logging
import pandas as pd
from datetime import datetime

from bases.interfaces.loader import LoadInterface
from config.settings import DB_PATH

logger = logging.getLogger(__name__)


class ScrappingLoader(LoadInterface):
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.ensure_db_directory()
        self.conn = duckdb.connect(self.db_path)
        self.ensure_sequence()
        self.create_table()
    
    def ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.debug("📁 Diretório criado para o banco de dados: %s", db_dir)

    def ensure_sequence(self):
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS news_id_seq START 1;")
        logger.debug("🔢 Sequência 'news_id_seq' verificada/criada com sucesso.")

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER DEFAULT nextval('news_id_seq'),
                data_importacao TIMESTAMP,
                tipo VARCHAR,
                titulo VARCHAR,
                url VARCHAR,
                data_noticia TIMESTAMP,
                PRIMARY KEY (id)
            )
        """
        self.conn.execute(create_table_query)
        logger.info("🧱 Tabela 'news' criada/verificada no banco: %s", self.db_path)
    
    def do_load(self, **kwargs) -> bool:
        """Carrega os dados transformados no banco de dados."""
        try:
            data_transformed = kwargs.get('data_transformed', {})
            if not data_transformed:
                logger.warning("⚠️ Nenhum dado fornecido para carregamento.")
                return False
            
            news_list = data_transformed.get('data', [])
            metadata = data_transformed.get('metadata', {})
            
            if not news_list:
                logger.info("ℹ️ Nenhuma notícia válida para carregar.")
                return True
            
            logger.info("💾 Iniciando carregamento de %d notícias no banco...", len(news_list))
            
            df = self._create_dataframe(news_list)
            self._insert_dataframe_to_db(df)
            
            logger.info("✅ %d notícias inseridas no banco com sucesso!", len(news_list))
            logger.debug(
                "📊 Totais — Originais: %d | Válidas: %d | Filtradas: %d",
                metadata.get('total_original', 0),
                metadata.get('total_valid', 0),
                metadata.get('total_filtered', 0),
            )
            
            return True
            
        except Exception as e:
            logger.exception("❌ Erro durante o carregamento: %s", e)
            return False

        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
    
    def _create_dataframe(self, news_list):
        """Converte lista de notícias em DataFrame."""
        current_time = datetime.now()
        
        data = [{
            'data_importacao': current_time,
            'tipo': n.get('tipo_noticia', ''),
            'titulo': n.get('titulo_noticia', ''),
            'url': n.get('url_noticia', ''),
            'data_noticia': n.get('data_noticia', None)
        } for n in news_list]
        
        df = pd.DataFrame(data)
        try:
            df['data_noticia'] = pd.to_datetime(df['data_noticia'], errors='coerce')
        except Exception:
            logger.warning("⚠️ Falha ao converter coluna 'data_noticia' para datetime.")
        
        logger.debug("🧾 DataFrame criado com %d registros e %d colunas.", len(df), len(df.columns))
        return df
    
    def _insert_dataframe_to_db(self, df):
        """Insere DataFrame no banco de forma segura."""
        self.conn = duckdb.connect(self.db_path)
        self.ensure_sequence()

        self.conn.register("temp_df", df)

        insert_query = """
            INSERT INTO news (data_importacao, tipo, titulo, url, data_noticia)
            SELECT data_importacao, tipo, titulo, url, data_noticia
            FROM temp_df
        """
        self.conn.execute(insert_query)
        logger.info("✅ %d registros inseridos na tabela 'news'.", len(df))
    
    def get_total_records(self):
        """Retorna o total de registros na tabela."""
        try:
            self.conn = duckdb.connect(self.db_path)
            result = self.conn.execute("SELECT COUNT(*) FROM news").fetchone()
            total = result[0] if result else 0
            logger.debug("📈 Total de registros na tabela 'news': %d", total)
            return total
        except Exception as e:
            logger.exception("❌ Erro ao consultar total de registros: %s", e)
            return 0
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
    
    def get_recent_news(self, limit=100):
        """Retorna as notícias mais recentes."""
        try:
            self.conn = duckdb.connect(self.db_path)
            query = """
            SELECT data_importacao, tipo, titulo, url, data_noticia
            FROM news 
            ORDER BY data_importacao DESC 
            LIMIT ?
            """
            result = self.conn.execute(query, (limit,)).fetchall()
            logger.debug("📰 %d notícias recentes retornadas.", len(result))
            return result
        except Exception as e:
            logger.exception("❌ Erro ao consultar notícias recentes: %s", e)
            return []
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
    
    def get_news_as_dataframe(self, limit=None):
        """Retorna as notícias como DataFrame."""
        try:
            self.conn = duckdb.connect(self.db_path)
            query = "SELECT * FROM news ORDER BY data_importacao DESC"
            if limit:
                query += f" LIMIT {limit}"
            df = pd.read_sql_query(query, self.conn)
            logger.debug("📊 DataFrame retornado com %d registros.", len(df))
            return df
        except Exception as e:
            logger.exception("❌ Erro ao consultar notícias como DataFrame: %s", e)
            return pd.DataFrame()
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
    
    def get_news_by_type(self, news_type, limit=None):
        """Retorna notícias filtradas por tipo."""
        try:
            self.conn = duckdb.connect(self.db_path)
            query = "SELECT * FROM news WHERE tipo = ? ORDER BY data_importacao DESC"
            if limit:
                query += f" LIMIT {limit}"
            df = pd.read_sql_query(query, self.conn, params=(news_type,))
            logger.debug("🧩 %d notícias retornadas do tipo '%s'.", len(df), news_type)
            return df
        except Exception as e:
            logger.exception("❌ Erro ao consultar notícias por tipo: %s", e)
            return pd.DataFrame()
        finally:
            if hasattr(self, 'conn'):
                self.conn.close()
