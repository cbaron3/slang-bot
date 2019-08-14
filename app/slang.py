import requests
from bs4 import BeautifulSoup
from app.config import PRAWConfig

URBANDICT_URL_DEFINE = 'https://www.urbandictionary.com/define.php?term='
def build_url( term : str):
    return URBANDICT_URL_DEFINE + term

def site_autocomplete( url:str ):
    """ 
        Returns the website url urbandictionary has loaded for a url.
        This is required because for a definition, sometimes the urban dictionary
        site auto capitalizes and changes spacings which ends up effecting the html parsing.
            Ex: Netflix and chill vs Netflix and Chill 

        Every urban dictionary define site makes a request and stores its own url as a href in a <link>
        tag with a canonical rel
    """
    data = requests.get( url )
    soup = BeautifulSoup( data.text, 'html.parser')
    page_nav = soup.find("link",{"rel":"canonical"})['href']
    return page_nav

def top_definition( url:str ):
    """ Get top definition for some term """
    data = requests.get( url )
    soup = BeautifulSoup( data.text, 'html.parser')
    contents = soup.find( 'div', { 'id': 'content' } )
    definition_panels = soup.find_all( 'div', {'class': 'def-panel'} )

    title = definition_panels[0].find( 'a', {'class': 'word'} ).text
    meaning = definition_panels[0].find( 'div', {'class': 'meaning'} ).text
    example = definition_panels[0].find( 'div', {'class': 'example'} ).text
    return title, meaning, example

def define( term : str):
    term = term.replace(' ', '%20')
    term = site_autocomplete( build_url( term ) )
    return top_definition( term )

if __name__ == "__main__":
    url = site_autocomplete( build_url( 'yeet' ) )
    print( top_definition( url ) )