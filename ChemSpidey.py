#!/usr/bin/env python
#
#!/usr/bin/python2.4
#
# 
"""ChemSpidey - a ChemSpider robot for Wave.

Gives you the an image of a named chemical for text in a blip. Heavily dependant on
'Grauniady' the Guardian API Robot written by Chris Thorpe
"""

__author__ = 'cameron.neylon@stfc.ac.uk (Cameron Neylon)'

from waveapi import events
from waveapi import model
from waveapi import robot
import waveapi.document as doc
import re

import ChemSpiPy

def SetManualLink(blip, text, url):
    """Aims to find text in the passed blip and then create link via setting annotation."""

    contents = blip.GetDocument().GetText()
    if text in contents:
        r = doc.Range()
	r.start = contents.find(text)
        r.end = r.start + len(text)
	blip.GetDocument().SetAnnotation(r, 'link/manual', url)



def OnBlipSubmitted(properties, context):
    blip = context.GetBlipById(properties['blipId'])
    contents = blip.GetDocument().GetText()
    key = '(chem)'
    leftdelim = '(\\[)'
    querysize = '(.[1,20])'
    optintspacer = '(;)?'
    optfloat = '(\\d*\\.\\d*)?'
    optunits = '(.[1,2])?'
    optional  = optintspacer + optfloat + optunits
    rightdelim = '(\\])'

    compiledregex = re.compile(key+leftdelim+querysize+optional+rightdelim, re.IGNORECASE|re.DOTALL)
    usertextlist = compiledregex.finditer(contents)

    if usertextlist != None:
        count = 0
        changeslist = []
        for chemicalname in usertextlist: 
            r = doc.Range(0,0)
            r.start = chemicalname.start()
            r.end = chemicalname.end() + 1
            query = chemicalname.group(2)
            compound = ChemSpiPy.simplesearch(query)
            url = "http://www.chemspider.com/Chemical-Structure.%s.html" % compound
            insert = query + " (csid:" + compound 
                if chemicalname.group(5) != None and chemicalname.group(6) == 'mg':
                    millimoles = float(chemicalname.group(5))/compound.molweight
                    insert.append(" " + millimoles + " millimoles")

                if chemicalname.group(5) != None and chemicalname.group(6) == 'g':
                    moles = float(chemicalname.group(5))/compound.molweight
                    insert.append(" " + moles + " moles")

            insert.append(")")
                    
            changeslist.append([r, insert, compound, url])
            count = count + 1

        while count != 0:
            count = count - 1
            blip.GetDocument().SetTextInRange(changeslist[count][0], changeslist[count][1])
            SetManualLink(blip, changeslist[count][2], changeslist[count][3]) 
            

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hello, I'm ChemSpidey, I will convert text of the form chem:chemicalName: to a link to ChemSpider")



if __name__ == '__main__':
  ChemSpidey = robot.Robot('cameronneylon-test',
                         image_url='http://www.chemspider.com/ImagesHandler.ashx?id=236',
			 version = '2',
                         profile_url='http://www.google.com')
  ChemSpidey.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  ChemSpidey.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)

  ChemSpidey.Run(debug=True)
