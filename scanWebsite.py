def scan_website(url):
  with open('out.txt', 'w', encoding='utf-8') as f:
      f.write('')
      
  def pageScan(url0):
    import requests,re
    from bs4 import BeautifulSoup
    from bs4 import Comment
    if not url0.endswith('/'):
        url0 += '/'
    page = requests.get(url0)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html5lib')
        comm = soup.findAll(text=lambda text:isinstance(text, Comment))
        [cm.extract() for cm in comm]
        tags = soup.select("a['href']")
        links = [tag['href'] for tag in tags if tag['href'].startswith(url) or tag['href'].startswith(url.replace('http','https')) or not tag['href'].startswith('http')]
        if links:
          links = [link if link.startswith(url) else url+re.findall(r'\W*(\w.*)',link)[0] for link in links if re.findall(r'\W*(\w.*)',link)]
          links = list(set(links))
          alltags = soup.findAll(text=True)
          visable_tags = [t for t in alltags if t.parent.name not in ['style','nav', 'script','script', 'head', 'title', 'meta','nav','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
          text = ' '.join([re.sub(r'[\n\s\r\t/]+',' ', t) for t in visable_tags])
          text = re.sub(r'\s+', ' ', text)
          text = re.sub(r'<\!--.*-->','',text)
          with open('out.txt', 'a+', encoding='utf-8') as f:
              f.seek(0)
              t = f.read()
              if text not in t:
                f.seek(0,2)
                f.write(text+'\n')
          for link in links:
              if link not in link_warehouse:
                print(link,' ', link in link_warehouse, len(link_warehouse))
                link_warehouse.append(link)
                try:
                  pageScan(link)
                except:
                  continue
    return

  if not url.endswith('/'):
    url += '/'
  if not url.startswith('http'):
    url = 'http://'+ url
  link_warehouse = [url]
  pageScan(url)

  
url = 'http://www.example.com/'
scan_website(url)
