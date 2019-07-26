import requests
from bs4 import BeautifulSoup

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


# def add_pg( url:str, page:int ) -> str:
#     return url + '&page=' + str(page)

# def all_definitions( url:str ):
#     """ Return all html pages for a given url """
    
#     pg_url = add_pg( url, 2 )
#     print(pg_url)
#     data = requests.get( pg_url )

#     print( get_current_page( data ) )
#     print( get_last_page( data ) )

# def get_current_page( data ):
#     soup = BeautifulSoup( data.text, 'html.parser')
#     page_nav = soup.find( 'div', { 'class': 'pagination-centered' } )
#     page = soup.find( 'ul', {'class':'pagination'} ).find( 'li', {'class': 'current' } )
#     print(page)
#     return page.find('a').text

# def get_last_page( data ):
#     soup = BeautifulSoup( data.text, 'html.parser')
#     page_nav = soup.find( 'div', { 'class': 'pagination-centered' } )
#     page = soup.find( 'ul', {'class':'pagination'} ).find_all( 'li' )
#     return page[-1].find('a', href=True)['href'] 

# class Definition:
#     def __init__(self, word, meaning, example, contributor, upvote, downvote ):
#       self.word = word
#       self.meaning = meaning
#       self.example = example
#       self.contributor = contributor
#       self.upvote = upvote
#       self.downvote = downvote

# class DefineResult:
#     """ 
#         DefineResult is a class that stores the result of a web request to a certain urban
#         dictionary term
#     """
#     URL = 'https://www.urbandictionary.com'
#     DEFINE = '/define.php?term='

#     def __init__( self, term:str ):
#         # Replace spaces cause it reduces 500 server errors
#         term = term.replace(' ', '%20')
#         # Base url
#         self.url = URL + DEFINE + term
#         # List of definitions
#         self.definitions = []

#     # TODO: Handle errors on requests.get better
#     # Scan the term definitions and parse them
#     def scan( ):
#         # Step 1: Fixing url so that it uses the canonical url
#         # Step 2: Get last page url by using URL + get_last_page()
#             # Step 2a: modify get_last_page to return only the page number and not the href element
#         # Step 3: Generate start and end url for limits of requests
#             # IMPROVE: Add a max definitions to get
#         # Step4: For each page, add all definition objects
#         pass

# def definitions( url:str ):
#     """ Get top definition for some term """
#     data = requests.get( url )
#     soup = BeautifulSoup( data.text, 'html.parser')
#     contents = soup.find( 'div', { 'id': 'content' } )
#     definition_panels = soup.find_all( 'div', {'class': 'def-panel'} )

#     #for def_panel in definition_panels:
#         # Title
#         #print( 'Title: {0}'.format(def_panel.find( 'a', {'class': 'word'} ).text ))
#         # Meaning works fine
#         #print( 'Meaning: {0}'.format(def_panel.find( 'div', {'class': 'meaning'} ).text ))
#         # Examples are wonky
#         #print( 'Example: {0}'.format(def_panel.find( 'div', {'class': 'example'} ).text ))
#         # Contributor
#         #print( 'User: {0}'.format(def_panel.find( 'div', {'class': 'contributor'} ).find('a').text ))
#         # Votes seem weird. The page refreshes itself one initial load up and the upvotes update after the refresh
#         #print( 'Upvote: {0}'.format(def_panel.find( 'a', {'class': 'up'} ).find('span').text ))
#         #print( 'Downvote: {0}'.format(def_panel.find( 'a', {'class': 'down'} ).find('span').text ))
#         #print()