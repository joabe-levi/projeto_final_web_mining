import argparse, sys
from pathlib import Path

# Caminho do projeto e do diretório src
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

# Garante que o Python reconhece o src como módulo raiz
for path in (PROJECT_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    
from scrapping.pipeline import ScrappingPipeline
from api.pipeline import YFinancePipeline
from config.logging import setup_logging

setup_logging()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Executa pipelines de scraping e ETL para o projeto."
    )
    parser.add_argument(
        "--scrapping",
        action="store_true",
        help="Executa apenas o pipeline de scraping."
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Executa apenas o pipeline da API."
    )
    return parser


def run_scrapping_pipeline():
    """Executa o pipeline de scraping."""
    print("Iniciando pipeline de scraping...")
    
    # Agora o pipeline instancia automaticamente as classes ETL
    pipeline = ScrappingPipeline()
    pipeline.run()
    print("Pipeline de scraping concluído!")


def run_api_pipeline():
    """Executa o pipeline da API."""
    print("Iniciando pipeline da API...")
    pipeline = YFinancePipeline()
    pipeline.run()
    print("Pipeline da API concluído!")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # Se nenhum argumento foi passado, executa todos os pipelines
    if not args.scrapping and not args.api:
        print("Executando todos os pipelines...")
        run_scrapping_pipeline()
        run_api_pipeline()
        print("Todos os pipelines foram executados!")
        return

    # Executa apenas o pipeline de scraping se especificado
    if args.scrapping:
        run_scrapping_pipeline()
    
    # Executa apenas o pipeline da API se especificado
    if args.api:
        run_api_pipeline()


if __name__ == "__main__":
    main()
