import requests
import re
from bs4 import BeautifulSoup
from bs4 import Comment
import csv
import argparse
parser = argparse.ArgumentParser(description="A argument is required: count")
parser.add_argument("count", type=int, help="Amount of pages scraped at once")
args = parser.parse_args()


def preRequest():
    
    url = "http://www.nla.gov.au/apps/ilrs/?action=IlrsSearch"
    print('\trequest to ' + url)
    data = {'nuc': '', 
            'term': '', 
            'termtype': 'Keyword', 
            'state': 'All', 
            'dosearch': 'Search', 
            'chunk': args.count}
    page = requests.post(url, data=data)
    soup = BeautifulSoup(page.content, 'html.parser')
    h1 = soup.find("h1")
    if(h1.string == 'SUMMARY RESULTS'):
        return {
            'totalCount': h1.next_sibling.next_sibling.span.string,
            'cookies': page.cookies.get_dict()
        }
    else:
        return {
            'totalCount': -1,
            'cookies': ''
        }
def getIDs(pageId, cookies):
    ids = []
    url = "http://www.nla.gov.au/apps/ilrs/"
    data = {'nuc': '', 
            'term': '', 
            'termtype': 'Keyword', 
            'state': 'All', 
            'dosearch': 'Search', 
            'action': 'IlrsSearch',
            'mode': 'display',
            'chunk': pageId}
    print('\trequest to ' + url)
    page = requests.post(url, data=data, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')
    h1 = soup.find("h1")
    if(h1.string == 'SUMMARY RESULTS'):
        for tag in h1.parent.table.find_all('a', href=re.compile("^/apps/ilrs/\?action=IlrsDetails&service_id=")):
            match = re.match("^/apps/ilrs/\?action=IlrsDetails&service_id=([0-9]+)", tag['href'])
            ids = ids + [match.group(1)]
    return ids

def getInfo(url):
    result = {'Company_Name': '', 'Address': '', 'Telephone': '', 'Facsimile': '', 'Email': '', 'Website': ''}
    print('\trequest to ' + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    main_table = soup.find('table', width="450")

    ################ Get Company_Name #################
    rows = main_table.find('table').find_all('tr')
    result["Company_Name"] = rows[0].find_all('td')[1].text.strip() + " " + rows[1].text.strip()
    
    ################ Get Website #################
    p_cont = main_table.find('hr').next_sibling.next_sibling
    if(p_cont.find('a')): result["Website"] = p_cont.find('a')['href']

    ################ Get Address #################
    b_address = main_table.find('b', string=re.compile("Main address:"))
    p_address = b_address.parent
    comments = p_address.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        c.extract()
    origin = p_address.find('b', string=re.compile("Main address:"))
    origin.extract()
    result['Address'] = p_address.text.strip().replace('\n' , ' ')
    
    ################ Get Email #################
    b_email = main_table.find('b', string=re.compile("ILL email:"))
    if(b_email): result['Email'] = b_email.next_sibling.next_sibling.text.strip()
    
    ################ Get Telephone #################
    b_phone = main_table.find('b', string=re.compile("ILL phone:"))
    if(b_phone): result['Telephone'] = b_phone.next_sibling.strip()
    
    ################ Get Facsimile #################
    b_fax = main_table.find('b', string=re.compile("ILL fax:"))
    if(b_fax): result['Facsimile'] = b_fax.next_sibling.strip()

    return result

input_file = csv.DictReader(open("data.csv"))
existIds = [row['ID'] for row in input_file]

dict_writer = csv.DictWriter(open('data.csv', 'a+', newline=''), ["ID", "Company_Name", "Address", "Telephone", "Facsimile", "Email", "Website"])
if(len(existIds) == 0): dict_writer.writeheader()


print('preparing to scrapy')
rlt = preRequest()
pageCount = (int(rlt['totalCount']) - 1 + args.count) // args.count
if(rlt['totalCount'] != -1):
    print('\tI found %s services in %d pages.' % (rlt['totalCount'], pageCount))
else:
    print('\terror during preparation')
    exit()


for pageId in list(range(1, pageCount)):
    print("checking %d/%d page" % (pageId, pageCount))
    ids = getIDs(pageId, rlt['cookies'])
    print("\tfound following %d ids" % (len(ids)))
    print("\t" + repr(ids))
    for id in ids:
        if(id in existIds):
            continue
        url = "http://www.nla.gov.au/apps/ilrs/?action=IlrsDetails&service_id=" + id
        info = getInfo(url)
        info["ID"] = id
        print('\t\tCompany Name: ' + repr(info['Company_Name']))
        dict_writer.writerow(info)
