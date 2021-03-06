#!/usr/bin/env python
# -*- encoding:utf-8 -*

from django.shortcuts import render

from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import loader,Context,RequestContext
from models import *
import urllib2
import json
import time
import redis
import commands
import chardet
# Create your views here.

command = "curl -H 'Content-Type: application/json' -X %s -d '%s' %s"

def index(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  #if request.method == 'GET':
  #  hostinfolist = HostInfo.objects.filter(Used=1).order_by('HostName')
  #  context={'hostinfolist':hostinfolist}
  #return render_to_response('used_hostinfo.html', locals(), RequestContext(request))
  return HttpResponseRedirect("/codis/codiscounter/")

def search(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  if request.method == 'POST':
    text = request.POST.get("text", "")
    hostinfolist = HostInfo.objects.filter(HostName__contains=text).order_by('HostName')
    for index, hostinfo in enumerate(hostinfolist):
      hostinfolist[index].no = index+1
    context={'hostinfolist':hostinfolist}
  return render_to_response('used_hostinfo.html', locals(), RequestContext(request))

def used(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  if request.method == 'GET':
    hostinfolist = HostInfo.objects.filter(Used=1).order_by('HostName')
    for index, hostinfo in enumerate(hostinfolist):
      hostinfolist[index].no = index+1
    context={'hostinfolist':hostinfolist}
  else:
    text = request.POST.get("text", "")
    isIP = True
    for c in text:
      if (c < '0' or c > '9') and c != '.':
        isIP = False
        break
    if text.find('.') < 0:
      isIP = False

    if isIP:
      hostinfolist = HostInfo.objects.filter(HostIP__contains=text).order_by('HostName')
      if not text.startswith('.'):
        text = '.' + text
      if not text.endswith('.'):
        text += '.'
      print "text="+text
      result = []
      for hostinfo in hostinfolist:
        ip = hostinfo.HostIP
        ip = '.' + ip + '.'
        if ip.find(text) >= 0:
          print ip
          result.append(hostinfo)
      hostinfolist = result
      for index, hostinfo in enumerate(hostinfolist):
        hostinfolist[index].no = index+1
      context={'hostinfolist':hostinfolist}
    else: 
      hostinfolist = HostInfo.objects.filter(HostName__contains=text).order_by('HostName')
      for index, hostinfo in enumerate(hostinfolist):
        hostinfolist[index].no = index+1
      context={'hostinfolist':hostinfolist}
    
  return render_to_response('used_hostinfo.html', locals(), RequestContext(request))

def unused(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  if request.method == 'GET':
    hostinfolist = HostInfo.objects.filter(Used=0).order_by('HostID')
    context={'hostinfolist':hostinfolist}
  return render_to_response('unused_hostinfo.html', locals(), RequestContext(request))

def login(request):
  return render_to_response('login.html', locals(), RequestContext(request))

def login2System(request):
  username = request.POST.get("username", "")
  password = request.POST.get("password", "")
  if (username == "admin" and password == "123456") or (username == "user" and password == "user"):
    request.session["username"] = username
    return HttpResponseRedirect("/codis/")
  else:
    mess = "password error!"
    context={"mess":mess}
    return render_to_response('login.html', locals(), RequestContext(request))

def logout(request):
  if "username" in request.session:
    del request.session['username']
  return render_to_response('login.html', locals(), RequestContext(request))


def dashboardurl(request, ip):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  url = "http://" + ip + "/admin"
  response = urllib2.urlopen(url)
  dashboard = response.read() 
  innerIP = ip
  #with open("/home/work/CodisCenter/codisapp/templates/dashboard.html", "w") as f:
  #  f.write(dashboard)
  return render_to_response('dashboard.html', locals(), RequestContext(request))
  
def dashboardurl_new(request, ip):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  url = "http://" + ip + ":8080/admin"
  response = urllib2.urlopen(url)
  dashboard = response.read() 
  innerIP = ip
  #with open("/home/work/CodisCenter/codisapp/templates/dashboard.html", "w") as f:
  #  f.write(dashboard)
  return render_to_response('dashboard_new.html', locals(), RequestContext(request))

def proxy(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  url = request.path
  innerUrl = url.replace("/proxy/", "http://")
  response = urllib2.urlopen(innerUrl)
  data = response.read()

  return HttpResponse(data)
  
def codishelp(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  url = request.path
  if url[-1] != '/':
    url += '/'
  ip = url.split('/')[-2]
  url = url[0:url.rfind(ip)]
   
  innerUrl = "http://" + ip + url
  response = urllib2.urlopen(innerUrl)
  data = response.read()

  hrefList = [
              "/api/remove_fence", 
              "/api/action/gc",
              "/test/zkdump",
              "/api/resusagestat",
              "/slots",
              "/api/overview",
              "/api/hastatus",
              "/api/getmyip",
              "/api/zkslowlog",
              "/api/slotstatistic",
              "/api/getresusage",
              "/api/putidc",
              "/api/delidc",
              "/api/haturnon",
              "/api/haturnoff",
              "/api/server_groups",
              "/api/setbigreqsize/1048576",
             ]

  for href in hrefList:
    data = data.replace(('href="' + href ).encode('utf-8'), ('href="' + href + '/' + ip + "/").encode('utf-8'))

  return HttpResponse(data)


def slots(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  url = request.path
  if url[-1] != '/':
    url += '/'
  ip = url.split('/')[-2]
  url = url[0:url.rfind(ip)]
   
  innerUrl = "http://" + ip + url
  response = urllib2.urlopen(innerUrl)
  data = response.read()
  data = data.replace("/md5.js", "/codis/static/js/md5.js")
  data = data.replace("/utils.js", "/codis/static/js/utils.js")
  data = data.replace("/jquery.min.js", "/codis/static/js/jquery.min.js")
  data = data.replace("/underscore-min.js", "/codis/static/js/underscore-min.js")
  data = data.replace("/bootstrap.min.js", "/codis/static/js/bootstrap.min.js")
  data = data.replace("/bootstrap.min.css", "/codis/static/css/bootstrap.min.css")
  data = data.replace("/api/slots", "/api/slots/" + ip + "/")
  data = data.replace("/slotinfo", "/slotinfo/" + ip + "/")
  return HttpResponse(data)
  
def redisConfig(request, data):
  #context={'':hostinfolist}
  #return render_to_response('used_hostinfo.html', locals(), RequestContext(request))
  data = data[data.find("conf")+4:]
  datas = data.split("name:")
  #return HttpResponse(datas)
  conf = {}
  for d in datas:
    msg = d.split("value:")
    if len(msg) > 1:
      msg[0] = msg[0].split('\n')[0]
      msg[1] = msg[1].split('\n')[0]
      conf[str(msg[0])] = str(msg[1])
      
    else:
      conf[msg[0]] = ""
  context={'conf':conf}
  conf = sorted(conf.iteritems(), key=lambda d:d[0])
  #context={'datas':datas}
  return render_to_response('redisConf.html', locals(), RequestContext(request))

def redisStat(request, data):
  data = json.loads(data)
  data = sorted(data.iteritems(), key=lambda d:d[0])
  return render_to_response('redisStat.html', locals(), RequestContext(request))
   
def redisSlowlog(request, data):
  datas = data.split("id=")
  for index, d in enumerate(datas):
    datas[index] = "id=" + d
  datas = datas[1:]
  return render_to_response('redisSlowlog.html', locals(), RequestContext(request))

def zkgc(request, innerUrl):
  secs = request.GET.get("secs")
  dels = request.GET.get("del")
  innerUrl = innerUrl + "?secs=%s&del=%s" % (secs, dels) 
  response = urllib2.urlopen(innerUrl)
  data = response.read()
  return HttpResponse(data)

def resusagestat(request, data):
  data = data.replace("dashboard", "proxydashboard")
  datas = data.split("proxy")
  datas = datas[1:]
  for index, d in enumerate(datas):
    if not d.startswith("dashboard"):
      datas[index] = "proxy"+d
  return render_to_response('resusagestat.html', locals(), RequestContext(request))

def zkdump(request, data):
  datas = []
  length = data[0: data.find("/zk/codis")]
  datas.append(length)
  data = data[data.find("/zk/codis"):]
  array = data.split('/zk/codis')
  array = array[1:]
  for a in array:
    datas.append("/zk/codis" + a)
  return render_to_response('zkdump.html', locals(), RequestContext(request))

def slotstatistic(request, data):
  infos = []
  datas = data.split("group:")
  for index, d in enumerate(datas):
    if index > 0:
      datas[index] = "group:" + d
    items = datas[index].split(",")
    for i in items:
      infos.append(i)
    infos.append('--------------------------------------------------------------------------------------------------------------------------------------------------------------------')
  datas = infos
 
  return render_to_response('slotstatistic.html', locals(), RequestContext(request))

def api(request):
  global command
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  url = request.path
  #print "url='" + url + "'"
  if url[-1] != '/':
    url += '/'
  ip = url.split('/')[-2]
  url = url[0:url.rfind(ip)]
   
  innerUrl = "http://" + ip + url
  if url.find("gc") >= 0:
    print "innerUrl=" + innerUrl
    print "ip='" + ip + "'"
    print "url='" + url + "'"
    #return HttpResponse("")
    return zkgc(request, innerUrl)
  data = ""
  if request.method == "GET":
    response = urllib2.urlopen(innerUrl)
    data = response.read()
    if url.find("redis") >= 0 and url.endswith("config/"):
      return redisConfig(request, data)
    groupID = request.GET.get("group_id", "-1")
    if url.find("redis") >= 0 and url.endswith("stat/") and groupID == "-1":
      return redisStat(request, data)
    if url.find("redis") >= 0 and url.find("slowlog") >= 0:
      return redisSlowlog(request, data)
    if url.find("resusagestat") >= 0:
      return resusagestat(request, data)
    if url.find("zkdump") >= 0:
      return zkdump(request, data)
    if url.find("slotstatistic") >= 0:
      return slotstatistic(request, data)
  elif request.method == "POST" and username == "admin":
    data = commands.getoutput(command %("POST", request.body, innerUrl))
  elif request.method == "PUT" and username == "admin":
    data = commands.getoutput(command %("PUT", request.body, innerUrl))
  elif request.method == "DELETE" and username == "admin":
    data = commands.getoutput(command %("DELETE", request.body, innerUrl))
  else:
    return HttpResponse("")
    
  return HttpResponse(data)
  
def codisInfo(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  codisInfoList = CodisInfo.objects.all().order_by('CodisID')
  for index, codisInfo in enumerate(codisInfoList):
    codisInfoList[index].no = index+1
  context={'codisInfoList':codisInfoList}
  return render_to_response('codisInfo.html', locals(), RequestContext(request)) 

def addHost(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  else:
    return render_to_response('addHost.html', locals(), RequestContext(request)) 
  
def addHost2db(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  
  ip = request.POST.get('ip', "")
  memory = request.POST.get('memory', "")
  room = request.POST.get('room', "")
  description = request.POST.get('description', "")

  hostInfo = HostInfo(HostIP=ip, HostMem=memory, Room=room, Used=0, Description=description)
  hostInfo.save()

  return HttpResponseRedirect("/codis/unused/addhost/")

def delHost(request, hostID):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  httpResponse=HttpResponse()
  hostInfo = None
  hostList = HostInfo.objects.filter(HostID=int(hostID))
  if hostList:
    hostInfo=hostList[0]
  else:
    result='没有此机器'
    httpResponse.write(result)
    return httpResponse
  hostInfo.delete()
  result='已经删除'
  httpResponse.write(result)
  return HttpResponseRedirect("/codis/unused/")

def updateHost(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")



def addCodis(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  return render_to_response('addCodis.html', locals(), RequestContext(request)) 

def addCodis2db(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  productname = request.POST.get('productname', "")
  dashboard = request.POST.get('dashboard', "")
  projectname = request.POST.get('projectname', "")
  rdowner = request.POST.get('rdowner', "")
  xyvip = request.POST.get('xyvip', "")
  yzvip = request.POST.get('yzvip', "")
  domain = request.POST.get('domain', "")
  description = request.POST.get('description', "")

  codisInfo = CodisInfo(ProductName=productname, Dashboard=dashboard, ProjectName=projectname, RdOwner=rdowner, XyVIP=xyvip, YzVIP=yzvip, Domain=domain, Description=description)
  codisInfo.save()

  return HttpResponseRedirect("/codis/addcodis/")

def updateCodis(request, codisID):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request))

  httpResponse=HttpResponse()
  codisInfo = None
  codisList = CodisInfo.objects.filter(CodisID=int(codisID))
  if codisList:
    codisInfo = codisList[0]
  else:
    result=u'没有此Codis'
    httpResponse.write(result)
    return httpResponse

  return render_to_response('updateCodis.html', locals(), RequestContext(request))

def updateCodis2DB(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request))
  
  codisid = request.POST.get('codisid', '') 
  productname = request.POST.get('productname', "")
  dashboard = request.POST.get('dashboard', "")
  projectname = request.POST.get('projectname', "")
  rdowner = request.POST.get('rdowner', "")
  xyvip = request.POST.get('xyvip', "")
  yzvip = request.POST.get('yzvip', "")
  domain = request.POST.get('domain', "")
  description = request.POST.get('description', "")

  CodisInfo.objects.filter(CodisID=int(codisid)).update(ProductName=productname, Dashboard=dashboard, ProjectName=projectname, RdOwner=rdowner, XyVIP=xyvip, YzVIP=yzvip, Domain=domain, Description=description)
  return HttpResponseRedirect("/codis/codisinfo/") 
  

def delCodis(request, hostID):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  httpResponse=HttpResponse()
  hostInfo = None
  hostList = CodisInfo.objects.filter(CodisID=int(hostID))
  if hostList:
    hostInfo=hostList[0]
  else:
    result=u'没有此Codis'
    httpResponse.write(result)
    return httpResponse
  hostInfo.delete()
  return HttpResponseRedirect("/codis/codisinfo/") 
  

def codisCounter(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  productList = []
  productDict = {}
  counter = {}
  codisInfoList = CodisInfo.objects.all().order_by('CodisID')
  for codisInfo in codisInfoList:
    productList.append(codisInfo.ProductName)
    productDict[codisInfo.ProductName] = codisInfo.Dashboard
    #value:业务名，机器数，codis总容量G，上周使用内存G，codis已用内存，一周数据增长率，剩余容量，容量使用率，key的个数，业务负责人
    counter[codisInfo.ProductName] =[codisInfo.ProjectName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,codisInfo.RdOwner]

  for product, dashboard in productDict.items():
    url = "http://" + dashboard + "/api/overview"
    print url
    try:
      response = urllib2.urlopen(url)
    except urllib2.URLError as err:
      continue
    strret = response.read()
    info = json.loads(strret) 
   
    totalKeyNum = 0
    totalUsedMem = 0
    totalMem = 0
    if product != "":
      totalMem = int(info["maxmemory"].split(".")[0])
    else:
      totalMem = int(info["product"].split(",")[2].split(".")[0])
    totalHostSet = set([])
    for redisInfo in info["redis_infos"]:
      keyNum = 0
      if redisInfo.has_key("db0"):
        keyNum = redisInfo["db0"].split(",")[0].split("=")[1]
      totalKeyNum += long(keyNum)
      mem = redisInfo["used_memory"]
      totalUsedMem += long(mem)
    #Codis总容量
    counter[product][2] = totalMem
    #Codis已用容量
    counter[product][4] = totalUsedMem/1024/1024/1024


    counter[product][6] = counter[product][2] - counter[product][4]
    counter[product][7] = int(counter[product][4] * 100 / counter[product][2])
    counter[product][7] = str(counter[product][7]) + "%"
    counter[product][8] = totalKeyNum
    if product != "":
      counter[product][9] = info["opsps"]
    else: 
      counter[product][9] = info["ops"]
    counter[product][10] = "无"

    url = "http://" + dashboard + "/api/server_groups"
    response = urllib2.urlopen(url)
    strret = response.read()
    info = json.loads(strret) 
   
    for group in info:
      for server in group["servers"]:
        redisip = server["addr"].split(":")[0]
        totalHostSet.add(redisip)
    counter[product][1] = len(totalHostSet)

    conn = redis.Redis("127.0.0.1", 6000)
    t = time.strftime("%Y-%m-%d",time.localtime(time.time() - 3600*24*7))
    key = "counter_" + t
    #上周使用量
    value = conn.hget(key, product)
    if value == None and product == "hundred":
      value = conn.hget(key, "hundre")
    if value != None:
      counter[product][3] = int(value)
      #一周数据增长率
      counter[product][5] = (counter[product][4] - counter[product][3]) * 100 / counter[product][3]
      counter[product][5] = str(counter[product][5]) + "%"

  context={'counter':counter, 'productList':productList, 'productDict':productDict}
  return render_to_response('codisCounter.html', locals(), RequestContext(request))


def publicCounter(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  prefixCounter = {}
  prefixList = []
  prefixInfoList = PublicPrefix.objects.all().order_by('PrefixID')
  for prefixInfo in prefixInfoList:
    prefixList.append(prefixInfo.PrefixName)
    prefixCounter[prefixInfo.PrefixName] = [prefixInfo.PrefixProject, 0, 0, prefixInfo.OpOwner, prefixInfo.RdOwner, prefixInfo.AccessTime]  

  conn = redis.Redis("127.0.0.1", 6000)
  for prefix in prefixList:
    prefixCounter[prefix][1] = conn.hget("public_keynum", prefix)
    prefixCounter[prefix][2] = conn.hget("public_keymem", prefix) 
 
  t = conn.get("public_counter_time")

  context={'counter':prefixCounter, "prefixList":prefixList, "t":t}
  return render_to_response('publicCounter.html', locals(), RequestContext(request))

def publicNoPrefix(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  text = []
  with open("public_noprefix.log", "r") as f:
    data = f.readlines()
    for d in data:
      text.append(d)
      

  conn = redis.Redis("127.0.0.1", 6000)
  t = conn.get("public_counter_time")
  num = conn.get("public_noprefix")
  context={'noprefix':text, "t":t, "num":num}
  return render_to_response('publicNoPrefix.html', locals(), RequestContext(request))

def monitor(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")

  productDict = {}
  codisInfoList = CodisInfo.objects.all().order_by('CodisID')
  for codisInfo in codisInfoList:
    productDict[codisInfo.ProductName] = codisInfo.Dashboard

  conn = redis.Redis("127.0.0.1", 6000)
  msg = conn.hgetall("codis_monitor")
  t = conn.get("codis_monitor_time")
  BigKeyDict = {}
  for productName, ip in productDict.items():
    r = conn.exists("BigKey_" + productName)  
    BigKeyDict[productName] = r
 
  context={'msg':msg, 't':t, 'productDict':productDict, "BigKeyDict":BigKeyDict}
  return render_to_response('codisMonitor.html', locals(), RequestContext(request))
  

def BigKey(request, productName):
  BigKeyList = []
  conn = redis.Redis("127.0.0.1", 6000)
  if conn.exists("BigKey_" + productName):
    result = conn.zrevrange("BigKey_" + productName, 0, -1, withscores=True)
    for r in result:
      key = r[0]
      length = int(r[1])
      idletime = conn.get(productName+"_"+key)
      #keytype = conn.get(productName+"_"+key+"_type")
      kv = [key, length, idletime]
      BigKeyList.append(kv)
  #print BigKeyList
  t = ""
  if conn.exists("BigKey_" + productName + "_time"):
    t = conn.get("BigKey_" + productName + "_time")
  else:
    t = "统计中..."
  context={'BigKeyList':BigKeyList, 'productName':productName, 't':t}
  return render_to_response('BigKey.html', locals(), RequestContext(request))
   

def addPrefix(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  return render_to_response('addPrefix.html', locals(), RequestContext(request)) 

def addPrefix2db(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return render_to_response('codisInfo.html', locals(), RequestContext(request)) 
  prefixname = request.POST.get('prefixname', "")
  prefixproject = request.POST.get('prefixproject', "")
  opowner = request.POST.get('opowner', "")
  rdowner = request.POST.get('rdowner', "")
  accesstime = request.POST.get('accesstime', "")
  description = request.POST.get('description', "")

  prefixInfo = PublicPrefix(PrefixName=prefixname, PrefixProject=prefixproject, OpOwner=opowner, RdOwner=rdowner, AccessTime=accesstime, Description=description)
  prefixInfo.save()

  return HttpResponseRedirect("/codis/addprefix/")

def prefixList(request):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  prefixInfoList = PublicPrefix.objects.all().order_by('PrefixID')
  for index, prefixInfo in enumerate(prefixInfoList):
    prefixInfoList[index].no = index+1
  context={'prefixInfoList':prefixInfoList}
  return render_to_response('prefixInfo.html', locals(), RequestContext(request)) 


def delPrefix(request, prefixID):
  if "username" not in request.session:
    return HttpResponseRedirect("/codis/login/")
  username = request.session["username"]
  if username != "admin":
    return HttpResponseRedirect("/codis/prefixlist/")
  httpResponse=HttpResponse()
  prefixInfo = None
  prefixList = PublicPrefix.objects.filter(PrefixID=int(prefixID))
  if prefixList:
    prefixInfo=prefixList[0]
  else:
    result=u'没有此前缀'
    httpResponse.write(result)
    return httpResponse
  prefixInfo.delete()
  return HttpResponseRedirect("/codis/prefixlist/") 



def ClusterReport(req):
  if "username" not in req.session:
    return HttpResponseRedirect("/codis/login/")

  productList = []
  productDict = {}
  counter = {}
  codisInfoList = CodisInfo.objects.all().order_by('CodisID')
  for codisInfo in codisInfoList:
    productList.append(codisInfo.ProductName)
    productDict[codisInfo.ProductName] = codisInfo.Dashboard
    #value:业务名，机器数，codis总容量G，上周使用内存G，codis已用内存，一周数据增长率，剩余容量，容量使用率，key的个数，业务负责人
    counter[codisInfo.ProductName] =[codisInfo.ProjectName, 0, 0, 0, 0, 0, 0, 0, 0,codisInfo.RdOwner]


  for product, dashboard in productDict.items():
    url = "http://" + dashboard + "/api/overview"
    print url
    try:
      response = urllib2.urlopen(url)
    except urllib2.URLError as err:
      continue
    strret = response.read()
    info = json.loads(strret) 
   
    totalKeyNum = 0
    totalUsedMem = 0
    totalMem = 0
    if product != "":
      totalMem = int(info["maxmemory"].split(".")[0])
    else:
      totalMem = int(info["product"].split(",")[2].split(".")[0])
    totalHostSet = set([])
    for redisInfo in info["redis_infos"]:
      keyNum = 0
      if redisInfo.has_key("db0"):
        keyNum = redisInfo["db0"].split(",")[0].split("=")[1]
      totalKeyNum += long(keyNum)
      mem = redisInfo["used_memory"]
      totalUsedMem += long(mem)
    #Codis总容量
    counter[product][2] = totalMem
    #Codis已用容量
    counter[product][4] = totalUsedMem/1024/1024/1024

    counter[product][6] = counter[product][2] - counter[product][4]
    counter[product][7] = int(counter[product][4] * 100 / counter[product][2])
    counter[product][7] = str(counter[product][7]) + "%"
    counter[product][8] = totalKeyNum

    url = "http://" + dashboard + "/api/server_groups"
    response = urllib2.urlopen(url)
    strret = response.read()
    info = json.loads(strret) 
   
    for group in info:
      for server in group["servers"]:
        redisip = server["addr"].split(":")[0]
        totalHostSet.add(redisip)
    counter[product][1] = len(totalHostSet)

    conn = redis.Redis("127.0.0.1", 6000)
    t = time.strftime("%Y-%m-%d",time.localtime(time.time() - 3600*24*7))
    key = "counter_" + t
    #上周使用量
    value = conn.hget(key, product)
    if value == None and product == "hundred":
      value = conn.hget(key, "hundre")
    if value != None:
      counter[product][3] = int(value)
      #一周数据增长率
      counter[product][5] = (counter[product][4] - counter[product][3]) * 100 / counter[product][3]
      counter[product][5] = str(counter[product][5]) + "%"

  context={'counter':counter, 'productList':productList, 'productDict':productDict}
  return render_to_response('ClusterReport.html', locals(), RequestContext(req))


def BigKvReport(req):
    if "username" not in req.session:
        return HttpResponseRedirect("/codis/login/")

    BigKeyTableDict = {}
    BigKeyLineList = []

    CodisInfoList = CodisInfo.objects.all().order_by('CodisID')
    r = redis.StrictRedis(host='127.0.0.1',port=6000)
    
    for c in CodisInfoList:
        if r.exists('BigKey_' + c.ProductName):
            BigKeyLineList = []
            BigKeyLineList.append(c.ProductName)
            BigKeyLineList.append(c.ProjectName)
            BigKeyLineList.append(c.RdOwner)
            bigkeycount = r.zcard('BigKey_' + c.ProductName)
            maxvaluekeyname = r.zrevrange('BigKey_' + c.ProductName, 0, 0, withscores=False)
            maxvalue = r.zscore('BigKey_' + c.ProductName, maxvaluekeyname[0])
            ##bigkeymaxvalue = r.zrevrange('BigKey_hundred', 0, 0, withscores=True)
            maxvalue_humen = round(maxvalue/1024/1024, 1)
            BigKeyLineList.append(bigkeycount)
            BigKeyLineList.append(maxvalue_humen)
            BigKeyTableDict[c.ProductName] = BigKeyLineList

    return render_to_response("BigKvReport.html", locals())


def BigKvDetailReport(req):
    if "username" not in req.session:
        return HttpResponseRedirect("/codis/login/")

    CodisInfoList = CodisInfo.objects.all().order_by('CodisID')
    r = redis.StrictRedis(host='127.0.0.1',port=6000)

    BigKvDetailDict = {}
    ClusterInfoDict = {}

    for c in CodisInfoList:
        if r.exists('BigKey_' + c.ProductName):
            bigkvlist = r.zrevrange('BigKey_' + c.ProductName, 0, 19, withscores=True)
            BigKvList_new = []
            for kv in bigkvlist:
                keyname = kv[0]
                length = round(kv[1]/1024/1024, 1)  #MB
                atime = r.get(c.ProductName + '_' + keyname)
                klist = [keyname, length, atime]
                BigKvList_new.append(klist)
            BigKvDetailDict[c.ProductName] = BigKvList_new

            if r.exists('BigKey_' + c.ProductName + '_time'):
                cluster_count_time = r.get('BigKey_' + c.ProductName + '_time')
            else:
                cluster_count_time = "统计中..."
            ClusterInfoList = [c.ProjectName, cluster_count_time]
            ClusterInfoDict[c.ProductName] = ClusterInfoList
            
    return render_to_response("BigKvDetailReport.html", locals())


