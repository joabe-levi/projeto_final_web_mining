from abc import ABC, abstractmethod


class LoadInterface(ABC):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @abstractmethod
    def do_load(self, **kwargs):
        """Carrega o DataFrame para o destino final"""
        pass
