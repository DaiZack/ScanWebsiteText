def scan_website(url,outfile='out.txt'):
  import requests,re
  from bs4 import BeautifulSoup
  from bs4 import Comment
  with open(outfile, 'w', encoding='utf-8') as f:
      f.write('')
  webstopwords = ['http','www','home','page','time','out','error','service','server','connect','fail','fobiden','skip','start','contact','email','facebook','read','more','help','hour','twitter','google','about','back','search','next','last','menu','news','blog','solution','address','phone','website','copyright','reserved','english']
      
  def pageScan(url0):
    page = requests.get(url0)

    if page.status_code != 200 and (not url0.endswith('/')):
      url0 += '/'
      page = requests.get(url0)
    if page.status_code == 200:

        soup = BeautifulSoup(page.content, 'html5lib')
        comm = soup.findAll(text=lambda text:isinstance(text, Comment))
        [cm.extract() for cm in comm]
        alltags = soup.findAll(text=True)
        visable_tags = [t for t in alltags if t.parent.name not in ['style', 'script','script','img', 'head', 'title', 'meta','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
        text = ' '.join([re.sub(r'[\n\s\r\t/]+',' ', t) for t in visable_tags])
        text = re.sub(r'\s+', ' ', text)
        print(page.status_code, ' : words', len(text))
        
        tags = soup.select("a['href']")
        links = [tag['href'] for tag in tags if tag['href'].startswith(url) or tag['href'].startswith(url.replace('http','https')) or not tag['href'].startswith('http')]
        if links:
          if not url0.endswith('/'):
            url0 += '/'
          links = [link if link.startswith(url) else url+re.findall(r'\W*(\w.*)',link)[0] for link in links if re.findall(r'\W*(\w.*)',link)]
          links = list(set(links))
          


          for sw in webstopwords:
            text = text.lower().replace(sw,'')
          with open(outfile, 'a+', encoding='utf-8') as f:
              f.seek(0)
              t = f.read()
              if text not in t:
                f.seek(0,2)
                f.write(text+'\n')
          for link in links:
              if link not in link_warehouse and '.pdf' not in link:
                link_warehouse.append(link)
                try:
                  pageScan(link)
                except:
                  continue
    else:
      print(url0,' : failed!')
    return

  if not url.endswith('/'):
    url += '/'
  if not url.startswith('http'):
    url = 'http://'+ url
  link_warehouse = [url]
  pageScan(url)
