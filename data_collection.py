import requests
from bs4 import BeautifulSoup
import re

# The article that we are going to search for.
article = 'Mario'

# Getting the response object using the article defined above.
res = requests.get('https://en.wikipedia.org/wiki/'+article)
article_html = res.content

# Making the BeautifulSoup object
webpage = BeautifulSoup(article_html,'html.parser')

# Finding the first paragraph using the logic defined in readme.md
article_bold_tag = webpage.select("p > b")[0]
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

# Printing the text for the link
for link_text in link_texts:
    if link_text in para_text:
        print(link_text)
        break

# Printing the url for the link for further use
for link in all_links:
    if link.text == link_text:
        print(link['href'])