#/usr/bin/env python
import json, os, urllib2, codecs

# 
# Script to export a dataset as json files into the filesystem
# 

WS = "http://api.gbif.org/v0.9"
PAGE_SIZE = 100
DATASET_NUB = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
DATASET_TEST = '2e38c085-1140-46b2-9fc3-c62fb18d56bf'
ROOTDIR = '/Users/mdoering/dev/backbone/kangchenjunga'


counter=0

def dumpUsage(u, parentDir):
  global counter
  # also dump common names and other extensions
  try:
    canonpath = os.path.join( parentDir, u.get("canonicalName","incertae sedis"))
    dirpath = canonpath
    idx=2
    while os.path.exists(dirpath):
      dirpath = canonpath + idx
      idx =+ 1
    os.makedirs(dirpath)
    fJson = codecs.open(os.path.join(dirpath,'data.json'), 'w','utf-8')
    fJson.write(json.dumps(u, sort_keys=True, indent=2, separators=(',', ': ')))
    fJson.close()
    
    # add defaults to json if None
    fReadme = codecs.open(os.path.join(dirpath,'README.md'), 'w','utf-8')
    fReadme.write(u"%s %s\n=======\nStatus: %s\nAccording to: %s\nPublished in: %s\n" % (u.get("rank","unranked"), u.get("scientificName","Name missing"), u.get("taxonomicStatus","???"), u.get("accordingTo","???"), u.get("publishedIn", "???")))
    fReadme.close()
  except Exception as e:
    print "  %s" % e
  counter =+ 1
  if (counter % 100 == 0):
    print "%s usages dumped\n" % (counter)
  iterUsages('/species/%s/children' %(u["key"]), dirpath)


def iterUsages(url, currDir):
  page=0
  usages = {"endOfRecords":False}
  while not usages["endOfRecords"]:
    usages = json.load(urllib2.urlopen('%s%s?limit=%s&offset=%s' %(WS,url,PAGE_SIZE,page*PAGE_SIZE)))
    for u in usages["results"]:
      dumpUsage(u, currDir)
    page += 1



# iterate over root usages
iterUsages('/species/root/%s' %(DATASET_NUB), ROOTDIR)
