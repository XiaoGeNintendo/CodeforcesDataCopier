try:
    import os
    import json
    import io
    import urllib.request
    from robobrowser import RoboBrowser
    import html
except Exception as err:
    print("Error 101:Import failed {0}".format(err))
    exit(101)


fromusr=""
tousr=""
topsd=""

b=RoboBrowser(parser="html.parser")

def getURL(url):
    print("Fetching From:"+url)
    request=urllib.request.Request(url)
    response=urllib.request.urlopen(request)
    html=response.read()
    return html.decode('utf-8')

def createCode(sub):
    try:
        print("Downloading Code")

        url=getURL("https://codeforces.com/contest/"+str(sub["contestId"])+"/submission/"+str(sub["id"]))

        code=url.split("""<pre id="program-source-text" class="prettyprint lang-cpp program-source" style="padding: 0.5em;">""")[1].split("</pre>")[0]

        
        code=html.unescape(code)
        
        f=open(str(sub["id"])+".sol","w")
        if "Py" not in sub["programmingLanguage"]:
            f.write(code+"//Transfer From {0} By XGN's Codeforces Transferer".format(str(sub["id"])))
        else:
            f.write(code+"#Transfer From {0} By XGN's Codeforces Transferer".format(str(sub["id"])))
            
        f.close()

        return True
    except Exception as err:
        print("Error downloading: {0}".format(err))
        return False    
    
def submit(sub):
    print("Submit for",sub["id"],"starts")
    
    b.open("https://codeforces.com/problemset/submit")
    form2=b.get_form(class_="submit-form")
    form2["submittedProblemCode"]=str(sub["contestId"])+sub["problem"]["index"]

    path=str(sub["id"])+".sol"
    
    try:
        if not os.path.exists(path):
            if not createCode(sub):
                raise Exception("Cannot download code!")
            
        form2["sourceFile"]=path
    except Exception as e:
        print("Error when selecting file {0}".format(e))
        return False

    lang=sub["programmingLanguage"]
    if "C++" in lang:
        form2["programTypeId"]="42"
    if "Java" in lang:
        form2["programTypeId"]="36"
    if "Py" in lang:
        form2["programTypeId"]="31"

    b.submit_form(form2)

    if b.url[-6:]!="status":
        print("Error when after submit")
        return False

    print("Successfully Submitted The Program",sub["id"])
    return True

print("Getting username and password")

fromusr=input("Username to Transfer=")

print("Reading sensitive data from files")
fr=open("usr.txt","r")
ln=fr.readlines()
tousr=ln[0].strip()
topsd=ln[1].strip()

# tousr=input("Username to Transfer to=")
# topsd=input("Password to Transfer to=")

print("Successfully get the users!",tousr[0]+"*"*(len(tousr)-1),"*"*len(topsd))

print("Getting all code from",fromusr)

try:
    res=json.loads(getURL("https://codeforces.com/api/user.status?handle="+fromusr+"&count=100"))
    if res["status"]!="OK":
        raise Exception("Bad status",res["status"])
except Exception as err:
    print("Error 202 Can't get API: {0}".format(err))
    exit(202)

fli=input("Filter for submissions(True for no filter)=")

ok=[]
for sub in res["result"]:
    if eval(fli):
        sub["ok"]=False
        ok.append(sub)
        print("OK submission:",sub["id"])
print("Filter done! To transfer submissions:",len(ok),"Not to transfer submissions:",len(res["result"])-len(ok))

op=input("Continue?[Y/N]")

if op!="Y" and op!="y":
    print("Exit 300 Stopped")
    exit(300)

print("Login with known username and password")
b.open("https://codeforces.com/enter")
form=b.get_form("enterForm")
form["handleOrEmail"]=tousr
form["password"]=topsd
b.submit_form(form)

if b.url=="https://codeforces.com/":
    print("Login Success!")
else:
    print("Error 201 Fatal Failure,Can't login! ->",b.url)
    exit(201)


for i in range(1,6):
    print("Try No.",i,"started")
    for x in ok:
        if x["ok"]:
            continue
        if submit(x):
            print("Submit Success",x["id"])
            x["ok"]=True
        else:
            print("Submit Failure",x["id"])

for i in ok:
    if not i["ok"]:
        print("Exit 203 Transfer failed.Maybe quota exceeded. Try again a few hours later!")
        f=open("secret.text","w")
        f.write(str(ok))
        f.close()
        exit(203)
        
print("Exit 0 Successfully transferred!")
exit(0)
