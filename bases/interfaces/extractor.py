from abc import ABC, abstractmethod


class ExtractInterface(ABC):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @abstractmethod
    def do_extract(self, **kwargs):
        """Extrai dados e retorna um DataFrame do Spark"""
        pass
