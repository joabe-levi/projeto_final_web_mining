import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class BaseCrawler:
    url = ''
    
    def __init__(self, **kwargs):
        self.time_to_wait = kwargs.get('time_to_wait', 0)
        self.headless = kwargs.get('headless', False)
        self.driver = None
    
    def _setup_driver(self):
        """Configura e instancia o driver do Chrome apenas quando necessário."""
        if self.driver is not None:
            return
            
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")

        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        options.add_argument(f'user-agent={user_agent}')
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(30)
    
    def close_driver(self):
        """Fecha o driver se estiver ativo."""
        if self.driver is not None:
            self.driver.quit()
            self.driver = None 

    def goto(self, url=None):
        """Navega para a URL especificada. Configura o driver se necessário."""
        self._setup_driver()
        if url:
            self.url = url
        return self.driver.get(self.url)

    def run(self):
        """Navigate to the configured URL and return the raw page source."""
        self._setup_driver()
        pass

    def get_page_source(self, url=None):
        """Obtém o código fonte da página. Configura o driver se necessário."""
        self._setup_driver()
        if url:
            self.url = url
            self.driver.get(self.url)
            
        if self.time_to_wait:
            time.sleep(self.time_to_wait)

        return self.driver.page_source
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - garante que o driver seja fechado."""
        self.close_driver()
    