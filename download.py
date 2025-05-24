import mechanicalsoup
import os
import os.path
import time
urlindex="https://s.bailushuyuan.org/%E9%9D%92%E9%93%9C%E8%91%B5%E8%8A%B1"
remove_tags=["script","meta","img","footer","link"]
urls_selector="ol.text-body-tertiary li a"
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
    maincontent=browser.page.select("article.card")[0];
    #clear(maincontent,remove_tags+["a"])
    #clear(browser.page,remove_tags+["a"])
    save(maincontent,os.path.join(title,href+".html"))
    i+=1
    #if i>5:
    #    break
      
      
save(mainpage,"index.html")
