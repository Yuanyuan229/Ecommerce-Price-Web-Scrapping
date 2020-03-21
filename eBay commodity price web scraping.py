#!/usr/bin/env python
# coding: utf-8

# <h1>Web-scraping: Which sellers advertise/sponsor on eBay
# 
# </h1>
# 
# 

# In[2]:


#import some libraries
import time
import requests,re
from bs4 import BeautifulSoup
import json
import pymysql as pymysql
import os


# In[5]:


def get_page_items(url):
    #imitate the action of real users
    time.sleep(10)
    #fetch the page content
    url= url
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r=requests.get(url,headers=kv)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        #Find the info of items and save the data to top_story
        item_list=soup.find('ul', "srp-results srp-list clearfix").find_all("li","s-item")
    except:
        print("failed")    
    return item_list


# In[10]:


def get_sponsored_unsponsored_items(item_list):
    sponsored_link=list()
    sponsored_name=list()
    unsponsored_link=list()
    unsponsored_name=list()
    for item in item_list:
        str_item=str(item)
        name = item.find('h3',"s-item__title").text
        try: 
            sponsor_element=item.find('div', "s-item__title--tagblock").text
            sponsor_ = re.findall(r'.*S.*P.*O.*N.*S.*O.*R.*E.*D.*', sponsor_element)
            if sponsor_ != []:
                link = re.findall('<a.+?class="s-item__link".+?href="(https:.+?)">',str_item)
                sponsored_link.append(link[0])
                sponsored_name.append(name)   
            else:
                link = re.findall('<a.+?class="s-item__link".+?href="(https:.+?)">',str_item)
                unsponsored_link.append(link[0])
                unsponsored_name.append(name)
        except:
            link = re.findall('<a.+?class="s-item__link".+?href="(https:.+?)">',str_item)
            unsponsored_link.append(link[0])
            unsponsored_name.append(name)
    return sponsored_name,sponsored_link,unsponsored_name,unsponsored_link


# In[11]:


#begin scraping 
#call the functions and find all sponsored and unpsonsored items & urls on page 1-10
all_s_links=list()
all_ns_links=list()
for page_num in range(10):
    url_ebay='https://www.ebay.com/sch/i.html?_nkw=playstation+4+slim&_pgn='+str(page_num+1)+'&LH_BIN=1&_ipg=100'
    pg_items=get_page_items(url_ebay)
    #get the sponsored and non-sponsored items
    s_name,s_link,ns_name,ns_link=get_sponsored_unsponsored_items(pg_items)
    for i in s_link:
        all_s_links.append(i) 
    for i in ns_link:
        all_ns_links.append(i)       


# In[12]:


#save the urls into txt files
def save_as_txt(name,link_list):
    f = open(name,'w')
    for i in range(len(link_list)):
        f.write(link_list[i])
        f.write('\n')
    f.close()
save_as_txt("sponsored.txt",all_s_links)
save_as_txt("non-sponsored.txt",all_ns_links)


# In[13]:


print("Get "+str(len(all_s_links))+" sponsored item urls!")
print("Get "+str(len(all_ns_links))+" non-sponsored item urls!")


# 
# <body>Create two folders in the same directory as your code and name them "sponsored" and "non-sponsored". 
# Write a program that opens the two files in (b) and downloads each of the pages (URLs) into the folders "sponsored" and "non- sponsored". 
# 
# Each file should be named as "<item-id>.htm" where you replace "item-id" with the ID of the item you are saving. E.g., "264616053293.htm" for the item with ID "264616053293". 
# 
# Note it is always good to put a 2-second pause between queries. 
# Make sure to catch an error and continue if your query runs into problems connecting to eBay (e.g., if your internet is down for 5 seconds, you don't want your entire code to crash).
# </body>

# In[14]:


# Create target Directory if not exist
def create_folder(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory: " , dirName ,  " Created ")
    else:    
        print("Directory: " , dirName ,  " already exists")
# create two folders
create_folder(os.getcwd()+"/sponsored")
create_folder(os.getcwd()+"/non-sponsored")

#get directory to the "sponsored" folder
dir_s=os.getcwd()+"/sponsored"
#get directory to the "non-sponsored" folder
dir_n=os.getcwd()+"/non-sponsored"


# In[15]:


def get_page(url):
    #imitate the action of real users
    time.sleep(2)
    #fetch the page content
    url= url
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r=requests.get(url,headers=kv)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print("failed")


# In[16]:


# save the web page
def save_page(name,content):
    f = open(name,'w')
    f.write(content)
    f.close()


# In[17]:


# find item id
def find_id(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    item_id = soup.find('div',"u-flL iti-act-num itm-num-txt").text
    return item_id


# In[18]:


#save sponsored item pages
#read the file line by line
f = open("sponsored.txt", "r")
line = f.readline()
cnt = 0
while line:
    cnt += 1
    try:
        pg_content=get_page(line)
        item_id=find_id(pg_content)
        name = dir_s+"/"+str(item_id)+".htm"
        #save the page
        save_page(name,pg_content)
        if cnt % 10 == 0:
            print("Saving "+str(cnt)+" non-sponsored item page...")
        # next url
        line = f.readline()
    except Exception as e:
        print("Error happened while saving "+str(cnt)+" sponsored item page") 
        print("Error message:{}".format(e))
        pass
print("Finish saving sponsored items!")
f.close()


# In[20]:


#save non-sponsored item pages
#read the file line by line
f = open("non-sponsored.txt", "r")
line = f.readline()
cnt = 0
while line:
    cnt += 1
    try:
        pg_content=get_page(line)
        item_id=find_id(pg_content)
        name = dir_n+"/"+str(item_id)+".htm"
        #save the page
        save_page(name,pg_content)
        if cnt % 20 == 0:
            print("Saving "+str(cnt)+" non-sponsored item page...")
        # next url
        line = f.readline()
    except Exception as e:
        print("Error happened while saving "+str(cnt)+" non-sponsored item page")
        print("Error message:{}".format(e))
        pass
print("Finish saving non-sponsored items!")
f.close()


# 
# Separate piece of code that loops through the pages you downloaded, open and parse them into a Python Beautifulsoup-object. Identify and select:
# 
# <b>seller name, seller score, item price, # items sold, best offer available, title, returns allowed, shipping price, condition (e.g., used, new, like new, seller refurbished, ...).</b>
# 
# 

# In[30]:


def get_info(file_name):
    f = open(file_name, "r")
    content=f.read()
    soup = BeautifulSoup(content, 'html.parser')
    #Find the info of items and save
    info_list=[]
    #Find the info of items, convert to suitable data type and save
    
        
    #=========== Find the seller_name VARCHAR(100)=======================================
    try:
        seller_name=soup.find('div', "mbg vi-VR-margBtm3").find("span","mbg-nw").text.replace(u'\xa0',u'').replace(u'\n',u'').replace(u'\t',u'')
    except:
        seller_name= 'N/A'


    #=========== Find the seller_score int =======================================
    try:
        seller_score=re.findall(r'="feedback score: ([0-9]{0,9})"',str(soup.find('div', "mbg vi-VR-margBtm3")))[0]
        seller_score=int(seller_score)
    except:
        seller_score= 'NULL'


    #=========== Find the item_price INT (UNIT USD cents)=======================================
    try:
        item_price_info=re.findall(r'.*[0-9]{1,}[.][0-9]*',soup.find("span","notranslate").text.replace("\t",""))
        item_price=re.findall(r'([0-9]{1,}[.][0-9]*)',soup.find("span","notranslate").text)
        #detect the currency and exchange
        # 1 CAD = 0.75 USD            
        if item_price_info[0][:1] == "C":
            item_price=int(float(item_price[0])*100*0.75)
        # 1 GBP = 1.29 USD
        elif item_price_info[0][:1] == "G":
            item_price=int(float(item_price[0])*100*1.29)
        else:
            item_price=int(float(item_price[0])*100)
    except:
        item_price= 'NULL'


    #=========== Find the items_sold INT=======================================
    try:
        items_sold=soup.find("a","vi-txt-underline").text.replace(u'\xa0',u'').replace(u'\n',u'').replace(u'\t',u'').replace(u',',u'').strip("sold")
        items_sold=int(items_sold)
    except:
        items_sold= 'NULL'

    #=========== Find the best_offer_available VARCHAR(10) Y/N=======================================
    try:
        best_info=soup.find('div',"vi-bbox-dspn u-flL lable boLable").text
        best_=re.findall(r'Best Offer',best_info)
        if best_ !=[]:
            best_offer_available="Yes" 
        else:
            best_offer_available="No"
    except:
        best_offer_available= 'No'

    #=========== Find the title VARCHAR(200)=======================================
    try:
        title=soup.find('h1', "it-ttl").text.strip("Details about    ").replace(u'\xa0',u'').replace(u'\n',u'').replace(u'\t',u'').replace(u',',u'')
    except:
        title= 'N/A'

    #=========== Find the returns_allowed VARCHAR(10) Y/N=======================================
    try:
        returns_allowed_info=re.findall(r'([0-9]{0,4}) day',soup.find('td', "rpWrapCol").find('span',id="vi-ret-accrd-txt").text)
        if returns_allowed_info !=[]:
            returns_allowed="Yes" 
        else:
            returns_allowed="No"
    except:
        returns_allowed= 'No'

    #=========== Find the shipping_price INT=======================================
    try:
        shipping_info=re.findall(r'FREE',soup.find('span',id="shSummary").text)
        shipping_info_price=re.findall(r'([0-9]{1,}[.][0-9]*)',soup.find('span',id="shSummary").text)
        if shipping_info_price !=[]:
            shipping_price=int(float(shipping_info_price[0])*100)
        else:
            if shipping_info !=[]:
                shipping_price=int(0)
            else:
                shipping_price="NULL"   
    except:
        shipping_price='NULL'

    #=========== Find the condition VARCHAR(100)=======================================
    try:
        condition=soup.find("div","u-flL condText").text.replace(u'\xa0',u'').replace(u'\n',u'').replace(u'\t',u'')
    except:
        condition= 'N/A'

    #save all info
    info_list=[seller_name, seller_score, item_price, items_sold, best_offer_available, title, returns_allowed, shipping_price, condition]
    
    return info_list


# In[31]:


# save all sponsored item info
sponsored_item_info=[]
skip=0
save=0
print("Saving item info...")
for filename in os.listdir(dir_s):
    if filename.endswith(".htm"):
        try:
            info=get_info(dir_s+"/"+filename)
            sponsored_item_info.append(info)
            save+=1
        except:
            print("error,skip "+str(skip)+" item...")
            skip+=1
            pass
    else:
        continue
print("Saving finished, saved "+str(save)+" items, skiped "+str(skip)+" item(s).")


# In[32]:


# save all non-sponsored item info
non_sponsored_item_info=[]
skip=0
save=0
print("Saving item info...")
for filename in os.listdir(dir_n):
    if filename.endswith(".htm"):
        try:
            info=get_info(dir_n+"/"+filename)
            non_sponsored_item_info.append(info)
            save+=1
        except:
            print("error,skip "+str(skip)+" item...")
            skip+=1
            pass
    else:
        continue
print("Saving finished, saved "+str(save)+" items, skiped "+str(skip)+" items.")


# 
# <body>
# connect to SQL 
#     
# Create a database and name it "eBay". 
# Save the information of items into a single table named "eBay_items" 
# 
# This table contains both sponsored and non-sponsored information and have a column that specifies which item is sponsored/non-sponsored. 
# If an item misses ANY of the information, insert as NULL. 
# 
# Convert any price (item price and shipping price) into a "dollar-cent" format (e.g., convert $12.34 into 1234 and $12 into 1200. Make sure the two least significant digits are cents. If an item does not include cents in the price, insert zeros.) and insert the price as INT into the table.
# </body>

# In[33]:


#connect
conn=pymysql.connect(host='localhost',user='root')
cursor = conn.cursor()
print("Connected to mySQL!")

# create database & table
try:
    # create database
    DB_NAME = 'eBay'
    cursor.execute('DROP DATABASE IF EXISTS %s' %DB_NAME)
    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' %DB_NAME)
    cursor.execute('use eBay')
    # create table
    TABLE_NAME = 'eBay_items'
    cursor.execute('DROP TABLE IF EXISTS %s' %TABLE_NAME)
    cursor.execute('CREATE TABLE %s(sponsored_or_not VARCHAR(15),seller_name VARCHAR(100), seller_score int, item_price INT, items_sold INT, best_offer_available VARCHAR(10), title VARCHAR(200), returns_allowed VARCHAR(10), shipping_price INT, item_condition VARCHAR(100))'
                   %TABLE_NAME)             
    
except Exception as e:
    print("Exeception occured:{}".format(e))
    
print("Database and table created!")   
# close cursor
cursor.close()
# close DB connection
conn.close()


# In[34]:


#insert data

#connect
conn=pymysql.connect(host='localhost',user='root')
cursor = conn.cursor()
cursor.execute('use eBay')

# insert SPONSORED  info
print("Insert SPONSORED info...","\n")
save_s=0
skip_s=0
  
for item in sponsored_item_info:
    try:
        sqlQuery='INSERT INTO eBay_items values("sponsored",'
        sqlQuery=sqlQuery+'"'+str(item[0])+'",'                     +str(item[1])+','                    +str (item[2])+','                    +str (item[3])+','                    +'"'+str(item[4])+'",'                    +'"'+str(item[5])+'",'                    +'"'+str(item[6])+'",'                    +str (item[7])+','                    +'"'+str (item[8])+'")'
        cursor.execute(sqlQuery)
        save_s+=1
    
    except Exception as e:
        skip_s+=1
        print("\n","Error,skip "+str(skip_s)+" sponsored item...")
        print("Error message:{}".format(e),"\n")
        pass
    
print(str(save_s)+" sponsored item info saved!","\n")
        

# insert NON-SPONSORED  info
print("Insert NON-SPONSORED info...","\n")
save_n=0
skip_n=0

for item in non_sponsored_item_info:
    try:
        sqlQuery='INSERT INTO eBay_items values("non-sponsored",'
        sqlQuery=sqlQuery+'"'+str(item[0])+'",'                     +str(item[1])+','                    +str (item[2])+','                    +str (item[3])+','                    +'"'+str(item[4])+'",'                    +'"'+str(item[5])+'",'                    +'"'+str(item[6])+'",'                    +str (item[7])+','                    +'"'+str (item[8])+'")'
        cursor.execute(sqlQuery)
        save_n+=1
    except Exception as e:
        try:
            sqlQuery='INSERT INTO eBay_items values("non-sponsored",'
            sqlQuery=sqlQuery+'"'+str(item[0])+'",'                         +str(item[1])+','                        +str (item[2])+','                        +str (item[3])+','                        +'"'+str(item[4])+'",'                        +"'"+str(item[5])+"',"                        +'"'+str(item[6])+'",'                        +str (item[7])+','                        +'"'+str (item[8])+'")'
            cursor.execute(sqlQuery)
            save_n+=1
        except:
            skip_n+=1
            print("\n","Error,skip "+str(skip_n)+" non-sponsored item...")
            print("Error message:{}".format(e),"\n")
            pass 

print(str(save_n)+" non-sponsored item info saved!","\n")


# final check
count = cursor.execute('SELECT * FROM %s' %TABLE_NAME)
print ('total records:', cursor.rowcount,"\n")


conn.commit()
# close cursor
cursor.close()
# close DB connection
conn.close()


# 
# <body>
# 
# Run summary stats on each item. 
#     
# Print to the screen the mean, min, max, and mean for each column, grouped by "sponsor/non-sponsor" and "condition" (group by at the same time, not separately). For binary categorical columns, use 0-1 conversion. 
#     
# If it is NOT a numerical/binary categorical column, print to the screen the count of each category level. NULL values are ignored in statistic calculations.
# </body>

# **Run Queries**

# In[6]:


#connect
conn=pymysql.connect(host='localhost',user='root')
cursor = conn.cursor()
cursor.execute('use eBay')

#binary categorical columns, use 0-1 conversion

binary_col=['best_offer_available','returns_allowed']
for col in binary_col:
    sqlQuery1="UPDATE eBay_items SET "+col+" = 1 WHERE "+col+"='Yes'"
    sqlQuery0="UPDATE eBay_items SET "+col+" = 0 WHERE "+col+"='No'"
    sqlQuery_al="ALTER TABLE eBay_items MODIFY "+col+" int"
    cursor.execute(sqlQuery1)
    cursor.execute(sqlQuery0)
    cursor.execute(sqlQuery_al)
    
#Queries to show the summaries
colnames= ["sponsored_or_not",'seller_name','seller_score','item_price','items_sold','best_offer_available',
 'title','returns_allowed','shipping_price','item_condition']

#Run queries
cursor.execute('select * from eBay_items')
#get the data type of columns
desc=cursor.description

for i in range(len(colnames)):
    if desc[i][1]==3:
        sqlQuery="SELECT sponsored_or_not,item_condition,avg("+colnames[i]+"), min("+colnames[i]+"), max("+colnames[i]+"), std("+colnames[i]+") FROM eBay_items group by 1,2 "
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        print("\t\t\tSummary of",colnames[i] )
        print("=================================================================")
        print("sponsor/non-sponsor \t mean \t  min \t max \t standard deviation \t")
        for row in result:
            print("\t",row)
        print("=================================================================")
        print("\n")
    else:
        sqlQuery="select "+colnames[i]+",count(*) from eBay_items group by 1"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        print("\t\t\tSummary of",colnames[i] )
        print("=================================================================")
        print(colnames[i],"\t"+"count\t")
        for row in result:
            print("\t",row)
        print("=================================================================")
        print("\n")

conn.commit()


# In[5]:


#change binary categorical columns back
binary_col=['best_offer_available','returns_allowed']
for col in binary_col:
    sqlQuery_al="ALTER TABLE eBay_items MODIFY "+col+" varchar(10)"
    sqlQuery1="UPDATE eBay_items SET "+col+" = 'Yes' WHERE "+col+"= '1'"
    sqlQuery0="UPDATE eBay_items SET "+col+" = 'No' WHERE "+col+"='0'"
    cursor.execute(sqlQuery_al) 
    cursor.execute(sqlQuery1)
    cursor.execute(sqlQuery0)  
     
    
conn.commit()
# close cursor
cursor.close()
# close DB connection
conn.close()

