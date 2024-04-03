import asyncio
import aiohttp
from collections import namedtuple

class FirstRequest(namedtuple('FirstRequest', ['status', 'counter_items', 'requestverificationtoken', 'url', 'request_context'], defaults = [None for _ in range(5)])):
    pass

class Parametrs:

    perpage : int = 250
    max_items : int = 3500

    __slots__ = ('url', 'sort_by', 'search_with', 'artist', 'title', 'song', 'genre', 'r')

    def __init__(self) -> None:
        self.url : str = 'search'
        self.sort_by : str = 'BestMatch'
        self.search_with = None
        self.artist = None
        self.title = None
        self.song = None
        self.genre = None
        self.r = None

    @property
    def query_string_params(self):
        query_string_params_ = {
                'mod' :  'AP' if self.url == 'search' else 'AM',
                'ft' : 'LP Vinyl',
                'in' : 'In Stock',
                'sortCol' : self.sort_by,
                'q' : self.search_with,
                'aar' : self.artist,
                'aal' : self.title,
                'aso' :self.song,
                'agn' : self.genre,
                'r' : self.r
            }
    
        for param in list(query_string_params_.keys()):
            if query_string_params_[param] is None:
                query_string_params_.pop(param)
        return query_string_params_
    


class RequestForImportCDs:
    headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua' : '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile' : '?0',
            'sec-ch-ua-platform':'"Linux"',
            'Accept-Encoding' : 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
            }

    __slots__ = ('cookie_jar', 'all_pages', 'first_page', 'request_end', 'stop_requester')


    def __init__(self) -> None:
        self.cookie_jar = aiohttp.cookiejar.CookieJar()
        self.first_page = FirstRequest()
        self.request_end = True
        self.stop_requester = True
    
    
    def updater_headers(self) -> dict[str : str]:
        new_headers = self.headers.copy()
        new_headers['__requestverificationtoken'] = self.first_page.requestverificationtoken
        new_headers['X-Requested-With'] = 'XMLHttpRequest'
        new_headers['Referer'] = self.first_page.url
        new_headers['Request-Context'] = self.first_page.request_context
        return new_headers
    
    
    async def async_get_page(self, query_string_params : dict, new_headers : dict, long_request_id : str, page : int):
        query_string_params_ = query_string_params.copy()
        new_headers_ = new_headers.copy()
        query_string_params_['pageNum'] = str(page)
        async with aiohttp.ClientSession(cookie_jar = self.cookie_jar) as session:
            async with session.get('https://www.importcds.com/catalog/getgrid', headers = new_headers_, params = query_string_params_) as responce:
                pass
    

    async def first_page_of_search(self, parametrs : Parametrs): 

        while not self.request_end:
            await asyncio.sleep(0.25)

        self.stop_requester = False
        self.request_end = False
    
        self.cookie_jar.update_cookies({'perpage' : f'{parametrs.perpage}'})
        async with aiohttp.ClientSession(cookie_jar = self.cookie_jar) as session:
            async with session.get(url = f'https://www.importcds.com/{parametrs.url}',allow_redirects = False, headers = self.headers, params = parametrs.query_string_params) as first_request:
                first_request_context = await first_request.text()
                print(first_request)

s = Parametrs()
asyncio.run(RequestForImportCDs().first_page_of_search(s))