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
    delim = '(\\[.{1,40}\\])'

    usertextregex = re.compile(key+delim, re.IGNORECASE|re.DOTALL)
    usertextlist = usertextregex.finditer(contents)

    if len(usertextlist) > 0:
        for chemical in usertextlist: 
	    r = doc.Range(chemical.start, (chemical.end + 1))
	    query = contents[(r.start + len(key)): (r.end-1)]

		if r.end > r.start:
		    compound = ChemSpiPy.simplesearch(query)
		    url = "http://www.chemspider.com/Chemical-Structure.%s.html" % compound

		    insert = query + " (csid:" + compound  +")"
		    blip.GetDocument().SetTextInRange(r, insert)
		    SetManualLink(blip, compound, url) 

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hello, I'm ChemSpidey, I will convert text of the form chem:chemicalName: to a link to ChemSpider")



if __name__ == '__main__':
  ChemSpidey = robot.Robot('chemspidey',
                         image_url='http://www.chemspider.com/ImagesHandler.ashx?id=236',
			 version = '2',
                         profile_url='http://www.google.com')
  ChemSpidey.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  ChemSpidey.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)

  ChemSpidey.Run(debug=True)
