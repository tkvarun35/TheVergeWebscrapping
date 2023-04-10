from bs4 import BeautifulSoup
import requests,json,csv,sqlite3
from datetime import datetime
from os.path import exists




now = datetime.now()
date = now.strftime("%d%m%Y")


page = requests.get("https://www.theverge.com/")
if(page.status_code==200):
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.select_one("#__NEXT_DATA__").text
    data = json.loads(data)
    id=0
    all_articles=[]
    data=data['props']['pageProps']['hydration']['responses']
    conn = sqlite3.connect('articles.db')
    file_exists = exists(date+'_verge.csv')
    if(file_exists==False):
        csv_file=open(date+'_verge.csv', 'x', newline='')
    for i in data:
        for j in i['data']['community']['frontPage']['placements']:
            title=j['placeable']['title'] if j['placeable'] is not None else ''
            url=j['placeable']['url'] if j['placeable'] is not None else ''
            author=j['placeable']['author']['fullName'] if j['placeable'] is not None else ''
            publishDate=j['placeable']['publishDate'] if j['placeable'] is not None else ''
            cur=conn.cursor()
            cur.execute("SELECT * FROM ARTICLES WHERE Title='"+title+"'")
            rows = cur.fetchall()
            # print(len(rows))
            if url!='':
                id=id+1
                all_articles.append({
                 "ID": id if id is not None else '',
                 "Title": title if title is not None else '',
                 "URL": url if url is not None else '',
                 "Author": author if author is not None else '',
                 "Publish Date": publishDate if publishDate is not None else ''
              })
            keys = all_articles[0].keys()
            with open(date+'_verge.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(all_articles)
            if(len(rows)>0):
                continue
            if url!='':
                sql=("INSERT INTO ARTICLES (TITLE,URL,AUTHOR,PUBLISH_DATA) VALUES ('"+title+"','"+url+"','"+ author+"','"+publishDate+"' )")
                conn.execute(sql)
    conn.commit()
    conn.close()



        

else:
    print("Request not processed")
