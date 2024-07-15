import requests, re
import polars as pl
from bs4 import BeautifulSoup as Soup


def auto_regex(items):
    tokenizer = re.compile(r' \n | <[^\s>]* | > | </[^>]*> | \s[^=]*= | "[^"]*" | [^<>]+ ', re.VERBOSE)
    pattern = '^'
    for tok in tokenizer.findall(items[len(items)//2]):
        # print(tok)
        tok = re.escape(tok)
        for candidate in [f'{pattern}{tok}', f'{pattern}(.*){tok}', f'{pattern}(.*)']:
            if all(re.match(candidate, item) for item in items):
                if not candidate.endswith('(.*)(.*)'):
                    pattern = candidate
                break
    return pattern[1:]

def auto_scrape(url):
    response = requests.get(url, headers= {'User-Agent': ''})
    soup = Soup(response.text, 'html.parser')
    for tag in soup.find_all():
        children = [child.name for child in tag.contents if child.name]
        if len(set(children)) == 1 and len(children) > 10 and tag.text.strip():
            children = [str(child) for child in tag.contents if child.name]
            pattern = re.compile(auto_regex(children))
            df = [pattern.match(child).groups() for child in children]
            df = pl.DataFrame(df, orient='row')
            texts = []
            urls = []
            
            for c in df.columns:
                if sample := df[len(df)//2][c].item():
                    if sample[0] == ' ': continue
                    elif sample[:2] in ['"h', '<a']: urls.append(c)
                    elif sample[0] == '"': continue  
                    elif sample[:2] in ['<t', '<b', '<s', '</']: continue
                    else: texts.append(c)
            print(df[texts + urls])

auto_scrape('https://gall.dcinside.com/board/lists/?id=baseball_new11')