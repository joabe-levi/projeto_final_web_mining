import re
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bases.crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup


class InfoMoneyCrawler(BaseCrawler):
    url = "https://www.infomoney.com.br/ultimas-noticias/"
    LOAD_MORE_BUTTON = (
        By.XPATH,
        (
            "//button[contains(@class, 'flex items-center') "
            "and contains(@class, 'justify-center') "
            "and contains(@class, 'rounded-full')]"
        ),
    )
    ITEM_CONTAINER = (
        By.XPATH,
        (
            "//div[contains(@class, 'basis-1/4') "
            "and contains(@class, 'px-6') "
            "and contains(@class, 'md:px-0')]"
        ),
    )
    
    # Seletores para extrair dados das notícias
    NEWS_TYPE_SELECTOR = (
        By.XPATH,
        ".//span[contains(@class, 'text-xs') or contains(@class, 'text-sm') and contains(@class, 'font-medium')]"
    )
    
    NEWS_TITLE_SELECTOR = (
        By.XPATH,
        ".//h3[contains(@class, 'font-bold')] | .//h2[contains(@class, 'font-bold')] | .//a[contains(@class, 'font-bold')]"
    )
    
    NEWS_URL_SELECTOR = (
        By.XPATH,
        ".//a[@href]"
    )
    
    NEWS_DATE_SELECTOR = (
        By.XPATH,
        ".//time | .//span[contains(@class, 'text-xs') or contains(@class, 'text-sm')]"
    )
    
    def __init__(self, **kwargs):
        kwargs.update(time_to_wait=2)
        super().__init__(**kwargs)

    def run(self):
        """Executa o crawling e retorna os dados processados."""
        try:
            info = {
                'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.goto()
            self._ensure_minimum_items_loaded()
            page_source = self.get_page_source()
            info.update(data=self._parser(page_source))
            return info
        finally:
            pass

    def _ensure_minimum_items_loaded(self, minimum=100):
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(EC.presence_of_all_elements_located(self.ITEM_CONTAINER))
        except TimeoutException:
            return
        previous_total = len(self.driver.find_elements(*self.ITEM_CONTAINER))
        
        while previous_total < minimum:
            try:
                load_more = wait.until(EC.element_to_be_clickable(self.LOAD_MORE_BUTTON))
            except TimeoutException:
                break
            
            self._click(load_more)
            try:
                wait.until(
                    lambda driver: len(driver.find_elements(*self.ITEM_CONTAINER)) > previous_total
                )
            except TimeoutException:
                break
            
            previous_total = len(self.driver.find_elements(*self.ITEM_CONTAINER))
            
        print(f"Loaded {len(self.driver.find_elements(*self.ITEM_CONTAINER))} items.")

    def _parser(self, page_source):
        """Extrai dados estruturados das notícias da página."""
        soup = BeautifulSoup(page_source, 'html.parser')
        news_list = []
        
        # Encontra todos os containers de notícias
        news_containers = soup.find_all('div', class_=lambda x: x and 'basis-1/4' in x and 'px-6' in x and 'md:px-0' in x)
        
        for container in news_containers:
            try:
                news_data = self._extract_news_data(container)
                if news_data:
                    news_list.append(news_data)
            except Exception as e:
                print(f"Erro ao extrair dados de uma notícia: {e}")
                continue
        
        print(f"Extraídas {len(news_list)} notícias com dados completos.")
        return news_list
    
    def _extract_news_data(self, container):
        """Extrai dados específicos de um container de notícia."""
        news_data = {
            'tipo_noticia': self._extract_news_type(container),
            'titulo_noticia': self._extract_news_title(container),
            'url_noticia': self._extract_news_url(container),
            'data_noticia': self._extract_news_date(container),
        }
        
        # Só retorna se tiver pelo menos título e URL
        if news_data['titulo_noticia'] and news_data['url_noticia']:
            return news_data
        return
    
    def _extract_news_type(self, container):
        """Extrai o tipo/categoria da notícia."""
        type = None
        try:
            # Procura por spans com classes específicas que podem indicar categoria
            type_element = container.find('div', class_='line-clamp-1').find('div', class_='text-sm')
            if type_element:
                type = type_element.get_text(strip=True)

        except:
            pass

        return type

    def _extract_news_title(self, container):
        """Extrai o título da notícia."""
        title = None
        try:
            title_element = container.find('div', class_='md:line-clamp-3').find('a', class_='hover:underline')
            if title_element:
                title = title_element.get_text(strip=True)

        except:
            pass
    
        return title

    def _extract_news_url(self, container):
        """Extrai a URL da notícia."""
        url = None
        try:
            link_element = container.find('div', class_='md:line-clamp-3').find('a', class_='hover:underline')
            if link_element:
                url = link_element['href']
                if url.startswith('/'):
                    url = f"https://www.infomoney.com.br{url}"
        except:
            pass
        
        return url
    
    def _extract_news_date(self, container):
        """Extrai a data da notícia e converte formato relativo para absoluto."""
        date_text = None
        try:
            # Procura por elemento com a data relativa
            time_element = container.find('div', class_='text-wl-neutral-500')
            if time_element:
                date_text = self._convert_relative_to_absolute_date(time_element.get_text(strip=True))
            
        except Exception as e:
            pass
        
        return date_text
    
    def _convert_relative_to_absolute_date(self, relative_date_text):
        """Converte data relativa (ex: '53 minutos atrás') para data absoluta."""
        try:
            from datetime import datetime, timedelta
            
            text = relative_date_text.strip().lower()
            
            # Padrões para diferentes tipos de tempo relativo
            patterns = [
                # Minutos
                (r'(\d+)\s*minutos?\s*atrás?', 'minutes'),
                (r'(\d+)\s*min\s*atrás?', 'minutes'),
                # Horas
                (r'(\d+)\s*horas?\s*atrás?', 'hours'),
                (r'(\d+)\s*h\s*atrás?', 'hours'),
                # Dias
                (r'(\d+)\s*dias?\s*atrás?', 'days'),
                (r'(\d+)\s*d\s*atrás?', 'days'),
                # Semanas
                (r'(\d+)\s*semanas?\s*atrás?', 'weeks'),
                (r'(\d+)\s*sem\s*atrás?', 'weeks'),
                # Meses
                (r'(\d+)\s*meses?\s*atrás?', 'months'),
                (r'(\d+)\s*m\s*atrás?', 'months'),
            ]
            
            for pattern, unit in patterns:
                match = re.search(pattern, text)
                if match:
                    value = int(match.group(1))
                    now = datetime.now()
                    
                    if unit == 'minutes':
                        target_date = now - timedelta(minutes=value)
                    elif unit == 'hours':
                        target_date = now - timedelta(hours=value)
                    elif unit == 'days':
                        target_date = now - timedelta(days=value)
                    elif unit == 'weeks':
                        target_date = now - timedelta(weeks=value)
                    elif unit == 'months':
                        # Para meses, usamos aproximadamente 30 dias
                        target_date = now - timedelta(days=value * 30)
                    else:
                        return relative_date_text  # Retorna o texto original se não conseguir converter
                    
                    # Retorna a data formatada
                    return target_date.strftime('%Y-%m-%d %H:%M:%S')
            
            # Se não encontrou nenhum padrão, retorna o texto original
            return relative_date_text
            
        except Exception as e:
            print(f"Erro ao converter data relativa '{relative_date_text}': {e}")
            return relative_date_text

    def _click(self, element):
        try:
            element.click()
            
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

        try:
            self.driver.execute_script("window.scrollBy(0, 1000);")
        except:
            pass
