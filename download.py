import mechanicalsoup
import os
import os.path
import time
urlindex="https://www.yourbiquge.com/book/177725/"
remove_tags=["script","meta","img","footer","link","style"]
urls_selector="div.info-chapters  a"
title="aa"
browser=mechanicalsoup.StatefulBrowser();
browser.open(urlindex)
def clear(page,tags):
        for tag in tags:
                all=browser.page.find_all(tag)
                for  i in all:
                        i.decompose()
def save(page,filename):
    with open(filename,"wb") as f:
        f.write(bytearray("<html><body>".encode("ascii")));
        f.write(bytearray(page.encode("ascii")))
        f.write(bytearray("</body></html>".encode("ascii")))
       

mainpage=browser.page;       
if title=="":
    title=mainpage.title.text;
if not os.path.exists(title):
    os.mkdir(title)
urls=mainpage.select(urls_selector)
clear(mainpage,remove_tags)
i=0;
for url in urls:
    href=os.path.basename(url["href"])
    if os.path.exists(os.path.join(title,href)):
        continue;
    retry=3;
    while True:
        r=browser.follow_link(url)
        print(r.status_code)
        if r.status_code==200:
            break;
        time.sleep(1)
        retry=retry-1
    time.sleep(0.06)
    clear(browser.page,remove_tags+["a"])
    maincontent=browser.page.select("div.border3-2")[0];
    #clear(maincontent,remove_tags+["a"])
    #clear(browser.page,remove_tags+["a"])
    save(maincontent,os.path.join(title,href+".html"))
    i+=1
    url["href"]=href+".html"   
    #if i>5:
    #    break
      
      
save(mainpage,title+"/index.html")
