import webbrowser,sys,os,pprint
# ok
KEYWORDSG = {
  'brocade','dell','emc','fibre','fiber','ftserver','nas','netapp',' san','san/','storage','stratus','vrtx','xorux','snmp','compellent','iscsi'
}
# lernbedarf
KEYWORDSY = {
  'hyper-v','cloud','künstliche','msa','powershell','proxmox','python','bash'
}
# reicht evtl.
KEYWORDSB = {
  'vmware','vcenter','esx','linux','vm-ware','virtualbox','infrastruktur'
}
# no go
KEYWORDSR = {
  'O365','Office365','hpc','hpe','aruba','active directory','administra','android','ansible','atlassian','azure','avamar','virus','backup','bsi','c#','c++','cisco','citrix','commvault','compliance','confluence','container','css','cms','datacore','datensicherung','datenbank','devops',
  'disposition','documentum','docker',
'domain','dsgvo','einkäufer','elektriker','elektroniker','entwickler','entra','exchange','erp','firewall','governance','gpo','gruppenrichtlinien','helpdesk','horizon','hitachi','kanban','kaufmann','kpi','kubernetes','itil',
'ios','iso27','iso 27','java','jira','mdm','m365',
'mechatronik','networker','nimble','normen','nutanix',
'object-storage','oracle','outlook','php','projektmanager','pure','bereitschaft','rubrik',
'sap','sales','sccm','security','servicetechniker','sharepoint','synergy',
's3','sql','teams','telefonanla','terminalserver','terraform','ticket','unstruktur','wochenend','scrum','schichtd','vdi','vertrieb','verkäufer','vpn','webdesign','xen'
}
# falsch
KEYWORDSZ = {
  'chemi','dellen','sanit','energy storage','friseur','zahn','lack'
}
#-------------------------
def keycountupdate(key):
	res =keycount.setdefault(key,0)
	keycount.update({key:res+1})
	print(key,res)
	return
	

def colorline(l):
    #print(l)
    lcl = l.lower()
#---
    for key in KEYWORDSG:
      hle=0
      while lcl.find(key,hle) != -1:
        keycountupdate(key)
        pos=lcl.find(key,hle)
        le=len(key)
        lout= l[:pos]+'<span style="background-color:lime;">'+l[pos:pos+le]+"</span>"
        hle=len(lout)
        lout=lout+l[pos+le:]
        #print(lout)
        l=lout
        lcl = l.lower()
        pos=lcl.find(key)
#---
#---
    for key in KEYWORDSY:
      hle=0
      while lcl.find(key,hle) != -1:
        keycountupdate(key)
        pos=lcl.find(key,hle)
        le=len(key)
        lout= l[:pos]+'<span style="background-color:yellow;">'+l[pos:pos+le]+"</span>"
        hle=len(lout)
        lout=lout+l[pos+le:]
        #print(lout)
        l=lout
        lcl = l.lower()
        pos=lcl.find(key)
#---
#---
    for key in KEYWORDSB:
      hle=0
      while lcl.find(key,hle) != -1:
        keycountupdate(key)
        pos=lcl.find(key,hle)
        le=len(key)
        lout= l[:pos]+'<span style="background-color:aqua;">'+l[pos:pos+le]+"</span>"
        hle=len(lout)
        lout=lout+l[pos+le:]
        #print(lout)
        l=lout
        lcl = l.lower()
        pos=lcl.find(key)
#---
#---
    for key in KEYWORDSR:
      hle=0
      while lcl.find(key,hle) != -1:
        keycountupdate(key)
        pos=lcl.find(key,hle)
        le=len(key)
        lout= l[:pos]+'<span style="background-color:red;">'+l[pos:pos+le]+"</span>"
        hle=len(lout)
        lout=lout+l[pos+le:]
        #print(lout)
        l=lout
        lcl = l.lower()
        pos=lcl.find(key)
#---
#---
    for key in KEYWORDSZ:
      hle=0
      while lcl.find(key,hle) != -1:
        keycountupdate(key)
        pos=lcl.find(key,hle)
        le=len(key)
        lout= l[:pos]+'<span style="background-color:brown;">'+l[pos:pos+le]+"</span>"
        hle=len(lout)
        lout=lout+l[pos+le:]
        #print(lout)
        l=lout
        lcl = l.lower()
        pos=lcl.find(key)
#---
    fout.write(l)
    return

#-----------------------------------------

keycount= { "-dummy-":1 }
fout = open("hc.html","wt")
with open("h.html") as fin:
  for l in fin:
	  colorline(l)
#fin.close
fout.close

#keycounts=keycount
#keycounts=dict(sorted(keycount.items()))
keycounts=dict(sorted(keycount.items(),key=lambda item: item[1]))
with open("h.html","a") as fh:
	#fh.write("test")
	for x in keycounts:
		li=x+"="+str(keycounts[x])+"  <br>"
		fh.write(li)
		#pprint.pp(li,stream=fh)
		print(li)

keycount= { "-dummy-":1 }
fout = open("hc.html","wt")
with open("h.html") as fin:
  for l in fin:
	  colorline(l)
fout.close()
webbrowser.open('hc.html')
os._exit(0)
