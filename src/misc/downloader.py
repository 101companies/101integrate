import sys
import getpass
import gdata.docs.client

def getCSVsByKey(key, datafoldername, foldernames):
	client = gdata.docs.client.DocsClient()
	client.ClientLogin(raw_input("GMail username: ") + '@gmail.com', getpass.getpass("GMail password: "), "wise")
	print "Login successful!"
	indexResource = client.GetResourceById(key)
	for gid in range(1, len(foldernames) + 1):
		path = datafoldername + foldernames[gid - 1] + "/cache/Index.csv"
		print "Downloading into", path
		client.DownloadResource(indexResource, path, {'gid': gid, 'exportFormat': 'csv'})

getCSVsByKey(sys.argv[1], sys.argv[2], sys.argv[3:])
