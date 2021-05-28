import requests
from bs4 import BeautifulSoup
import re

def get_html(article:str):
    # Getting the response object using the article defined above.
    res = requests.get('https://en.wikipedia.org/wiki/'+article)
    article_html = res.content

    # Making the BeautifulSoup object
    webpage = BeautifulSoup(article_html,'html.parser')
    return webpage

#webpage = get_html(article)

def get_link(webpage_html):
    # Finding the first paragraph using the logic defined in readme.md
    article_bold_tag = webpage_html.select("p > b")[0]
    first_para_tag = article_bold_tag.parent

    # All the references inside the first paragraph
    all_links = first_para_tag.find_all('a')

    # The text in the first paragraph
    para_text = first_para_tag.text

    # Regex used to remove any links that are inside () or []
    forbidden_text_regex = re.compile('\(.*?\)|\[.*?\]')
    forbidden_text_list = forbidden_text_regex.findall(para_text)

    # Replacing the text inside brackets from the paragraph text
    for forbidden_text in forbidden_text_list:
        para_text = para_text.replace(forbidden_text,'')

    # The text present inside the links
    link_texts = [link.text for link in all_links]

    word_found = False
    word = None
    # Printing the text for the link
    for link_text in link_texts:
        if link_text in para_text:
            word_found = True
            word = link_text
            #word = link_text
            break

    # Printing the url for the link for further use
    for link in all_links:
        if link.text == word:
            word = link
            #print(link['href'])

    if word_found:
        return (word['href'],word_found)
    else:
        print('Word not found')
        return None

if __name__ == '__main__':
    # The article that we are going to search for.
    article = 'Creativity'
    webpage_html = get_html(article)
    link = get_link(webpage_html)
    print('https://en.wikipedia.org'+link[0])
