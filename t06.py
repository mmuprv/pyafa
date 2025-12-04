import requests
import pprint
import json
import subprocess
import sys,os,datetime

def stellen(liste):
	params = (
		('angebotsart', '1'),
		('page', '1'),
# true,false undef=ignore
#		('pav', 'false'),
# true,false undef=ignore
		('zeitarbeit', 'false'),
		('size', '100'),
		('umkreis', '50'),
	)
	headers = {
		'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
		'Host': 'rest.arbeitsagentur.de',
		'X-API-Key': 'jobboerse-jobsuche',
		'Connection': 'keep-alive',
	}

	st = liste['ergebnisliste']
	#pprint.pp(st)
	for x in st:
		ref = x['referenznummer']
		res = x.setdefault("alleBerufe"," --- ")
		res = x.setdefault("firma"," --- ")
#		res = x.setdefault("arbeitgeberKundennummerHash"," --- ")
# ignore externals!
		res = x.setdefault("arbeitgeberKundennummerHash","external")
		if res == "external":
			blacklist[ref]="external"
		#pprint.pp(x)
		flag="-none-"
		if ref in blacklist:
			flag=blacklist[ref]
		print(flag)
		if showheader == True:
			with open("h.html", "a") as f:
				f.write("<!DOCTYPE html><html><body><hr><hr><h1>"+x['referenznummer']+"   "+x['aenderungsdatum']+" "+x['hauptberuf']+" "+x['firma']+"<br>")	
				f.write("  Flag: "+flag+"\n")	
	#        f.write('<button onclick=\'Object.defineProperty(jobmap, \"'+ref+'\", {value:"noqual"});\'>objnoqual Export data to local txt file</button>\n')
	#        f.write('<button onclick=\'jobmap.set("'+ref+'","noqual")\'>noqual Export data to local txt file</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","-none-")\'>RESET-Flags</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","noqual")\'>No Qual</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","lowqual")\'>Low Qual</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","wrong")\'>Total Miss</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","closed")\'>Closed</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","closedqual")\'>Closed noQual</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","closedmoney")\'>Closed Money!</button>\n')
				f.write('<button onclick=\'bclick("'+ref+'","running")\'>Still running</button>\n')
				f.write("</h1><hr></body></html>\n")	
	#        pprint.pp(x, stream=f)
	#     f.write("<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p><hr></body></html>")	

		print("------------------------------------------------")
		print(x["referenznummer"], x['aenderungsdatum'],  x["hauptberuf"], x["alleBerufe"], x["firma"],flag)
#		if flag != "all":
#		if flag == "-none-":
#      if flag == "-none-" or flag == "running":
		if flag != "wrong" and flag != "noqual":
			if showheader == False:
				with open("h.html", "a") as f:
					f.write("<!DOCTYPE html><html><body><hr><hr><h1>"+x['referenznummer']+"   "+x['aenderungsdatum']+" "+x['hauptberuf']+" "+x['firma']+"<br>")	
					f.write("  Flag: "+flag+"\n")	
					f.write('<button onclick=\'bclick("'+ref+'","-none-")\'>RESET-Flags</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","noqual")\'>No Qual</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","lowqual")\'>Low Qual</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","wrong")\'>Total Miss</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","closed")\'>Closed</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","closedqual")\'>Closed noQual</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","closedmoney")\'>Closed Money!</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","running")\'>Still running</button>\n')
					f.write('<button onclick=\'bclick("'+ref+'","doit")\'>Contact!!!</button>\n')
					f.write("</h1><hr></body></html>\n")	

			jresponse = requests.get('https://rest.arbeitsagentur.de/vermittlung/ag-darstellung-service/pc/v1/arbeitgeberdarstellung/'+x['arbeitgeberKundennummerHash'], headers=headers, params=params, verify=True)
			#pprint.pp(jresponse.json(),width=132,compact=True)
			with open("h.html", "a") as f:
				pprint.pp(x, stream=f)
				f.write("<br>")
				pprint.pp(jresponse.json(),width=132,compact=True,stream=f)
			print("=============================================------------------------------------------------")
			print( subprocess.check_output("wget -O - 'https://www.arbeitsagentur.de/jobsuche/jobdetail/%s' >> h.html  " % x["referenznummer"], shell=True))
	return

def search(what, where):
	"""search for jobs. params can be found here: https://jobsuche.api.bund.dev/
	https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs?angebotsart=1&was=IT-Consultant&
	wo=44577&umkreis=50&sort=entfernung&veroeffentlichtseit=14&externestellenboersen=false&page=1&size=25&pav=false&facetten=false"""
	params = (
		('angebotsart', '1'),
		('page', '1'),
# true,false undef=ignore
		('pav', 'false'),
# true,false undef=ignore
		('zeitarbeit', 'false'),
		('size', '250'),
# max 200km
		('umkreis', '50'),
# min tage in db?
#		('veroeffentlichtseit', '99'),
# max tage
		('externestellenboersen', 'false'),
		('facetten', 'false'),
		('sort', 'moddatum'),
		('was', what),
		('wo', where))
	headers = {
		'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
		'Host': 'rest.arbeitsagentur.de',
		'X-API-Key': 'jobboerse-jobsuche',
		'Connection': 'keep-alive',
	}
#    response = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/app/jobs',
	response = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs', headers=headers, params=params, verify=True)
#    print(response.headers)
	rlist= response.json()
	#pprint.pp(rlist)
	print(json.dumps(rlist),"=============================")
	if rlist['maxErgebnisse'] ==0:
		rlist = json.loads("""{"ergebnisliste": [{"stellenangebotsart": "ARBEIT", "stellenangebotsTitel": "-dummy-", "arbeitszeitHeimarbeitTelearbeit": false,
		 "arbeitszeitSchichtNachtWochenende": false, "arbeitszeitTeilzeitAbend": false, "arbeitszeitTeilzeitNachmittag": false, "arbeitszeitTeilzeitVormittag": false,
		  "arbeitszeitTeilzeitFlexibel": false, "arbeitszeitVollzeit": true, "eintrittszeitraum": {"von": "2025-11-27"}, "verguetungsangabe": "KEINE_ANGABEN",
		   "vertragsdauer": "UNBEFRISTET", "istGeringfuegigeBeschaeftigung": false, "stellenlokationen": [{"adresse": {"strasse": "Limbecker Platz 1", "plz": "45127",
		    "ort": "Essen, Ruhr", "region": "NORDRHEIN_WESTFALEN", "land": "DEUTSCHLAND"}, "breite": 51.4562977, "laenge": 7.005481}],
		     "veroeffentlichungszeitraum": {"von": "2025-11-19"}, "datumErsteVeroeffentlichung": "2025-02-07", "aenderungsdatum": "2025-11-27T07:37:16.585",
		      "hauptberuf": "-dummy-", "firma": "-dummy-", "arbeitgeberKundennummerHash": "dMaqtmzMWBSTZMwIPPVr1PWQ3LHB7vF1NhXthhvHVjnU=", "referenznummer": "00018935-1666849-S",
		       "entfernung": 26, "alleBerufe": ["Ingenieur/in - Service/Instandhaltung"]}], "maxErgebnisse": 1, "page": 1, "size": 100,
		        "woOutput": {"bereinigterOrt": "44577", "suchmodus": "UMKREISSUCHE", "koordinaten": [{"lat": 51.5668577, "lon": 7.3306736}]}}""")
	stat= response.json()
	if stat['maxErgebnisse'] !=0:
		stat.pop('ergebnisliste')
	with open("h.html", "a") as f:
		f.write("<!DOCTYPE html><html><body><h2><hr><hr>")
		pprint.pp(params, stream=f)
		f.write("</h2><h3>")	
		pprint.pp(stat, stream=f)
		f.write("</h3><hr><hr></body></html>")	
	res = stellen(rlist)
	return rlist

def initjs():
    f = open("h.html","wt")
    f.write("<!DOCTYPE html><html><body><h1>Afa Jobs</h1>")	
    s='''
<script>
var jobmap = {};
//JSON.parse(\'{  "s": "ttttt",  "a": "bbbb",  "c": "ddd"}\');
// var jobmap = { "s":"ttttt", "a":"bbbb" ,c:"ddd"};

function bclick(key,val) {
  // jobmap.set(key,val);
  Object.defineProperty(jobmap, key, {value:val,writable:true,configurable:true,enumerable:true});
  //alert(key+":"+val);
}

function export2txt() {

  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(jobmap, null, 2)], {
    type: "text/plain"
  }));
  a.setAttribute("download", "pyafaadd.json");
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

function show() {
  let text = typeof(jobmap)+"= "+ Object.isExtensible(jobmap)+Object.isSealed(jobmap)+Object.isFrozen(jobmap);
  for (const x in jobmap) {
    text += x+":"+jobmap[x] + ", ";
  };
  alert(text+"...."+JSON.stringify(jobmap, null, 2));
}

</script>
'''
    f.write(s)
    f.write('<button onclick="export2txt()">Export Data to local ~/Downloads/pyafaadd.json file</button>')
    f.write('<button onclick="show()">ShowExport Data</button>')
    #f.write('<button onclick="writeDb(dataObj)">writeExport data to local txt file</button>')
    f.write("<hr><hr>")
    f.write(f'\n')
    f.close()
    return

def jsonimport():
	if os.path.exists("/home/myself/Downloads/pyafaadd.json"):
	  t=datetime.datetime.now()
	  #print(t)
	  print(subprocess.check_output("cp /home/myself/Downloads/pyafaadd.json '/home/myself/Downloads/pyafaadd.json.%s'" %t, shell=True))
	  print(subprocess.check_output("cp /home/myself/Downloads/pyafa.json '/home/myself/Downloads/pyafa.json.%s'" %t, shell=True))
    
	with open("/home/myself/Downloads/pyafa.json","rt") as f:
		db = f.read()
	bl=json.loads(db)
	if os.path.exists("/home/myself/Downloads/pyafaadd.json"):
		with open("/home/myself/Downloads/pyafaadd.json","rt") as f:
			db = f.read()
		bla=json.loads(db)
		bl.update(bla)
		os.remove("/home/myself/Downloads/pyafaadd.json")
		with open("/home/myself/Downloads/pyafa.json","wt") as f:
			f.write(json.dumps(bl))
	return bl
	
#-----------------------------------------
showheader=False
#showheader=True
blacklist=jsonimport()
initjs()
result = search("EMC", "44577")
result = search("Dell", "44577")
result = search("Compellent", "44577")
result = search("Fibre", "44577")
result = search("Fiber", "44577")
result = search("Netapp", "44577")
result = search("Storage", "44577")
result = search("SAN", "44577")
result = search("Systemarchitekt", "44577")
result = search("Systemanalytiker", "44577")
result = search("Systemberater", "44577")
result = search("IT-Systemberater", "44577")

result = search("IT-Berater", "44577")
result = search("IT-Consultant", "44577")

#result = search("IT-", "44577")
#result = search("EDV-", "44577")

print(subprocess.check_output("python3 cf02.py", shell=True))
sys.exit()

#others:
#https://www.bochumer-jobanzeiger.de/suche/?fulltext=it&locationIds=M-DE-11726&jobId=REG28329907
#https://www.jobware.de/job/059379607?jw_chl_seg=ARBEITSAGENTUR
#https://www.xing.com/jobs/dortmund-cio-145950041?utm_campaign=germanpersonnel&utm_content=145950041&utm_medium=jobboard_organic&utm_source=ba_vam
#https://www.get-in-it.de/jobsuche/p293254?utm_source=arbeitsagentur&utm_medium=cpc&utm_campaign=launch-basic
#https://www.jobboerse-direkt.de/
#https://www.kalaydo.de/jobs/15866207/?utm_id=ba&utm_source=bundesagentur&utm_medium=unpaid-partner&utm_campaign=000&campaign=ba
#https://www.finest-jobs.com/
#https://gute-jobs.de/viewjob-w8n2c?utm_source=jsba-premium&utm_medium=n-a&utm_campaign=jsba-premium&utm_term=it-engineer-als-tech-lead-technical-product-owner-m-w-d
#https://www.empfehlungsbund.de/jobs/289270/account-manager-w-strich-m-strich-d
#https://www.stellenanzeigen.de/job/detail/15866328/?utm_id=ba&utm_source=bundesagentur&utm_medium=unpaid-partner&utm_campaign=000&campaign=ba
#https://www.yourfirm.de/job/detail/20251124-28301442/?utm_campaign=free&utm_source=bundesagentur&utm_medium=unpaid-partner

#-----------------------------------------


#print(result['stellenangebote'][0]["refnr"])


#  jresponse = requests.get('https://www.arbeitsagentur.de/jobsuche/jobdetail/x["refnr"]')
#  pprint.pp(jresponse.content)
#  jresponse = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v2/jobdetails/'+x["refnr"], headers=headers, params=params, verify=True)
#  jresponse = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobdetails/MTAwMDEtMTAwMjIyNjgzNC1T', headers=headers, params=params, verify=True)

#, headers=headers, params=params, verify=True)
#  pprint.pp(jresponse.json(),width=132,compact=True)

pprint.pp(result)

#print(*(key for key in result))
#di = json.loads(result)
#print(di)
#['stellenangebote'])

# https://www.arbeitsagentur.de/jobsuche/jobdetail/10000-1194957357-S
