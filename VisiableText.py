def visiableText(page):
    from bs4 import BeautifulSoup, Comment
    import re
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in ['style', 'script','script','img', 'head', 'title', 'meta','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
    visible =  ' '.join([re.sub(r'[\n\s\r\t/]+',' ', t) for t in visable_tags])
    return re.sub(r'\s+', ' ', visible)
