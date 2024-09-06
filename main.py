import xml.etree.ElementTree as ET
import logging
import os
import time
import sys
import fileinput

from xml.etree.ElementTree import Element

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s %(sclname)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


scdfile='Busbar-Bay-Test-2-2.scd'
se="'Schneider Electric'"
sclns0='http://www.iec.ch/61850/2003/SCL'
sclns="{"+sclns0+"}"
ET.register_namespace('',sclns0)
ET.register_namespace('eIEC61850-6-100',"http://www.iec.ch/61850/2019/SCL/6-100")
ET.register_namespace('esel',"http://www.selinc.com/2006/61850")
ET.register_namespace('sxy',"http://www.iec.ch/61850/2003/SCLcoordinates")

logd = {'sclname': scdfile, 'user': 'fbadloggs'}

def RemoveAP(iedse, apname):
    logger.warning("Removing %s", apname, extra=logd)
    ap=iedse.find ("./" + sclns + "AccessPoint[@name='"+apname+"']")
    #iedse.remove(ap)
    return True

def CheckAP(apname):
    logger.warning("Checking %s", apname, extra=logd)


if not os.path.exists(scdfile):
    logger.error('File not found: %s', len(scdfile), extra=logd)
    logger.error('Fatal Error', extra=logd)
    exit(0)


file_name, file_extension = os.path.splitext(scdfile)
scdnewfile=f"{file_name}_{int(time.time())}.{file_extension}"


tree = ET.parse(scdfile)
root=tree.getroot()
ok=True
newScd=False

path1="./"+sclns+"IED[@manufacturer="+se+"]"
lse=root.findall(path1)


if len(lse)>1:
    logger.error('Unexpected SE IED: %d', len(lse), extra=logd)
    ok=False

if len(lse)==0:
    logger.error('No SE IED', extra=logd)
    ok=False

if not ok:
    logger.error('Fatal Error', extra=logd)
    exit(0)

# only one SE IED
iedse=lse[0]

pathAp1="./"+sclns+"AccessPoint[@name='AP1']/"+sclns+"Server/../.."
pathAp2="./"+sclns+"AccessPoint[@name='AP2']/"+sclns+"ServerAt/../.."
pathAp3="./"+sclns+"AccessPoint[@name='AP3']/"+sclns+"ServerAt/../.."

ap1=iedse.find(pathAp1)
ap2=iedse.find(pathAp2)
ap3=iedse.find(pathAp3)

if type(ap1) is None:
    logger.error('AP1 not OK', extra=logd)
    ok = False
else:
    CheckAP("AP1")

if type(ap2) is not None:
    logger.warning('Need to remove AP2', extra=logd)
    newScd2=RemoveAP(iedse, "AP2")
    if newScd is False:
        newScd=True

if type(ap3) is None:
    logger.error('AP3 not OK', extra=logd)
    ok = False
else:
    CheckAP("AP3")

if newScd is True:
    tree.write(scdnewfile,
           xml_declaration = True,
           encoding = 'utf-8',
           method = 'xml')
for i, line in enumerate(fileinput.input(scdnewfile, inplace=True)):
    sys.stdout.write(line.replace('&gt;', '>'))


#<OrderingCode xmlns="http://www.schneider-electric.com/IEC61850/XMLSchema">
#<GooseReceive xmlns="http://www.schneider-electric.com/IEC61850/XMLSchema">