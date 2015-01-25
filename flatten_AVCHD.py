#!/usr/bin/env python
#coding: utf8 

import os
import re
import fnmatch
import sys

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###
#

# Dieses Script passt die Struktur von AVCHD-Filmen an

# LETZTE ÄNDERUNG: 24.01.2015
# STATUS: funktioniert
# VERBESSUNGEN: Erkennung, ob AVCHD vorliegt, verbessern
#
### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

nzbName = os.environ['NZBPP_NZBNAME']
nzbDir = os.environ['NZBPP_DIRECTORY'] + '/'

isAVCHD = False

POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94

#----------------------------------------------------------------------
## Feststellen, ob AVCHD

if re.search(r'AVCHD', nzbName, re.M):
	isAVCHD = True
else:
	matches = []
	for root, dirnames, filenames in os.walk(nzbDir):
		for dirname in fnmatch.filter(dirnames, 'STREAM'):
			matches.append(os.path.join(root, dirname))
	if matches:
		isAVCHD = True

#-----------------------------------------------------------------------------
## Datei- und Pfadnamen zurecht basteln und Dateien verschieben

print 100*'-'

if isAVCHD:
	print 'AVCHD-Format erkannt'
	print 'Ordner-Hierarchie wird angepasst'

	# .m2ts-Dateien finden
	matches = []
	for root, dirnames, filenames in os.walk(nzbDir):
		for filename in fnmatch.filter(filenames, '*.m2ts'):
			matches.append(os.path.join(root, filename))

	for file in matches:
		# Pfad- und Dateinamen trennen
		pathAndFilename = re.search(r'^(.*/)(.*)$', file, re.M)

		path = pathAndFilename.group(1)
		file = pathAndFilename.group(2)

		# Dateinamen sollten 00000, 00001, 00002 lauten
		fileName = str(file).split('.')[0]
		
		# .m2ts
		fileExtension = '.' + str(file).split('.')[-1]
		
		# CD-Nummer vom Dateinamen ableiten
		cdNumber = 0
		try:
			if isinstance(int(fileName), int):
				cdNumber = int(fileName) + 1
		except:
			print '[ERROR] CD-Nummern können nicht vom Dateinamen abgeleitet werden!'
			sys.exit(POSTPROCESS_ERROR)
		
		# .m2ts-Files verschieben
		os.rename(path + fileName + fileExtension, nzbDir + nzbName + ' cd' + str(cdNumber) + fileExtension)

else:
	print '[INFO] kein AVCHD-Format erkannt - nichts zu tun'

#-----------------------------------------------------------------------------

print 100*'-'

sys.exit(POSTPROCESS_SUCCESS)