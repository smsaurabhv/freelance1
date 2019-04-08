from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
def getlogin():
    # Fill in your details here to be posted to the login form.
    payload = {
    'uNam': 'STROM',
    'uPwd': 'strom2017',
    'Loginning':'Sign In',
    '__EVENTTARGET':'' ,
    '__EVENTARGUMENT':'' 
    }
    sessioncreate = requests.Session()
    getdata = sessioncreate.get("http://www.ginlongmonitoring.com/LoginPage.aspx").content
    makesoup = BeautifulSoup(getdata,'html.parser')
    VIEWSTATE = makesoup.find("input",attrs={"id":"__VIEWSTATE"}).get("value")
    payload['__VIEWSTATE' ] = VIEWSTATE
    #print(VIEWSTATE)
    EVENTVALIDATION = makesoup.find("input",attrs={"id":"__EVENTVALIDATION"}).get("value")
    payload['__EVENTVALIDATION' ] = EVENTVALIDATION
    #print(EVENTVALIDATION)
    p = sessioncreate.post('http://www.ginlongmonitoring.com/LoginPage.aspx', data=payload)
    return sessioncreate



def getdata():
    print("pass the data")
    getloginobject  = getlogin()
    getallrow = []
    for k in range(1,100):
        getcontent = getloginobject.get('http://www.ginlongmonitoring.com/AjaxService.ashx?ac=pagemove&page='+str(k)+'&search=false&order=&upper=&datatype=&sitename=&country=&from=&to=&gateway=&sn=&custorname=').content
        parse = BeautifulSoup(getcontent,'html.parser')
        findre = parse.find_all("tr")
        if len(findre)==0:
                break
        for row in findre:
            print(row)
            getallrow.append(row)
    html = "<table>"
    for row in getallrow:
        print(row)
        html+=str(row)
    html+="</table>"
    print(html)
    return html


@app.route('/') 
def result():
    html = getdata()
    return render_template('home.html',data=html)
if __name__ == '__main__':
   app.run('0.0.0.0',port=2000)