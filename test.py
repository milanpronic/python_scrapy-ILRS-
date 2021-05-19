import requests
import re
from bs4 import BeautifulSoup
from bs4 import Comment
import csv
import argparse
parser = argparse.ArgumentParser(description="A argument is required: id")
parser.add_argument("id", help="Service_id to test")
args = parser.parse_args()

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

url = "http://www.nla.gov.au/apps/ilrs/?action=IlrsDetails&service_id=" + args.id
info = getInfo(url)
info["ID"] = args.id
print(info)