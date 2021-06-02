import requests
from bs4 import BeautifulSoup

def get_first5_ptags(article):
    res = requests.get('https://en.wikipedia.org/wiki/' + article)
    webpage_html = BeautifulSoup(res.content, 'html.parser')
    first5para_ptags = webpage_html.select('div#mw-content-text div.mw-parser-output > p')[:5]
    
    return first5para_ptags

def get_all_links(ptags):
    links_dict={}
    all_links = []
    for para in ptags:
        all_links_in_para = para.find_all('a')
        all_links.extend(all_links_in_para)
    
    for link in all_links:
        try:
            link_key = link.get_text(" ", strip=True)
            link_value = link['href']
            links_dict[link_key] = link_value
        except KeyError:
            print(link)
            
    return links_dict,all_links

def get_para_text(ptags):
    first5para_text = ''
    for para in ptags:
        first5para_text = first5para_text + para.get_text(" ", strip=True)
        
    return first5para_text

def get_clean_text(first5para_text):
    bracket_count = 0
    clean_text = ''
    for i in first5para_text:
        if i == '(' or i == '[':
            bracket_count += 1
        if i == ')' or i == ']':
            bracket_count -= 1
        if bracket_count == 0:
            clean_text += i
            
    return clean_text

def get_next_link(links, clean_text):
    clean_links = {}
    for index, key in enumerate(links):
        if key in clean_text and key != '':
            try:
                pos = clean_text.index(' '+key+' ')
                clean_links[pos] = key
            except ValueError:
                pass
            
    ans_key = clean_links[min(clean_links.keys())]
    ans = links[ans_key]
    return ans



if __name__ == '__main__':
    article = 'Pokémon'
    print('/wiki/'+article)
    first5_ptags = get_first5_ptags(article)
    links_dict,dirty_links = get_all_links(first5_ptags)
    dirty_text = get_para_text(first5_ptags)
    clean_text = get_clean_text(dirty_text)
    next_link = get_next_link(links_dict, clean_text)
    print(next_link)
    while next_link != '/wiki/Outline_of_philosophy' and next_link != '/wiki/Philosophy':
        next_article = next_link[6:]
        first5_ptags = get_first5_ptags(next_article)
        links_dict,dirty_links = get_all_links(first5_ptags)
        dirty_text = get_para_text(first5_ptags)
        clean_text = get_clean_text(dirty_text)
        next_link = get_next_link(links_dict, clean_text)
        print(next_link)

    print('/wiki/Philosophy')

    
    