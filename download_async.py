import os
import os.path
import time
import asyncio
import mechanicalsoup
from bs4 import  BeautifulSoup
import aiohttp
async def fetch(session, url):
    retry=3;
    while retry>0:
        async with session.get(url) as response:
          print(response.status)
          if response.status==200:
              return await response.text()
          else:
              retry=retry-1
    return ""

async def get_main_content(content):
       return content.select("div.border3-2")[0];
async def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Do something with the links
    return soup
async def clear(page,tags):
        for tag in tags:
                all=page.find_all(tag)
                for  i in all:
                        i.decompose()
        return True
async def save(page,filename):
    with open(filename,"wb") as f:
        f.write(bytearray("<html><body>".encode("ascii")));
        f.write(bytearray(page.encode("ascii")))
        f.write(bytearray("</body></html>".encode("ascii")))
    return True
async def main():
    urlindex="https://www.yourbiquge.com/book/177725/"
    baseurl="https://www.yourbiquge.com"
    remove_tags=["script","meta","img","footer","link"]
    urls_selector="div.info-chapters  a"
    title="aa"
    browser=mechanicalsoup.StatefulBrowser();
    browser.open(urlindex)
    mainpage=browser.page
    if title=="":
        title=mainpage.title.text;
    if not os.path.exists(title):
        os.mkdir(title)
    urls=mainpage.select(urls_selector)
    b=await clear(mainpage,remove_tags)
    i=0;
    async with aiohttp.ClientSession() as session:
        for url in urls:
            href=os.path.basename(url["href"])
            if os.path.exists(os.path.join(title,href)):
                continue;
            print(baseurl+"/"+href)
            content=await fetch(session,baseurl+"/"+url["href"])
            if len(content)>0:
                soup_content=await parse(content)
                b=await clear(soup_content,remove_tags+["a"])
                clear_c=await get_main_content(soup_content)
                b=await save(clear_c,os.path.join(title,href+".html"))
    i+=1
    url["href"]=href+".html"
    #if i>5:
    #    break
    b=await save(mainpage,title+"/index.html")


asyncio.run(main())
