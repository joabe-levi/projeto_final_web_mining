from abc import ABC


class PipelineInterface(ABC):
    def run(self):
        """Executa o pipeline e retorna os dados processados."""
        pass
