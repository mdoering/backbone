#/usr/bin/env python
import json, os, urllib2

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
  # also dump common names and other extensions
  try:
    dirpath = os.path.join( parentDir, u.get("canonicalName","incertae sedis"))
    os.makedirs(dirpath)
    
    fJson = open(os.path.join(parentDir,'data.json'), 'w')
    fJson.write(json.dumps(u, sort_keys=True, indent=2, separators=(',', ': ')))
    fJson.close()
    
    # add defaults to json if None
    fReadme = open(os.path.join(parentDir,'README.md'), 'w')
    fReadme.write("%s %s\n=======Status: %s\nAccording to: %s\n" % (u.get("rank","unranked"), u.get("scientificName","Name missing"), u.get("taxonomicStatus","???"), u.get("accordingTo","???")))
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
iterUsages('/species/root/%s' %(DATASET_TEST), ROOTDIR)
