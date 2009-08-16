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

import ChemSpiPy

#def SetManualLink(blip, text, url):
    #"""Aims to find text in the passed blip and then create link via setting annotation."""

    #blip = context.GetBlipByID(properties['blipID']
    #contents = blip.GetDocument().GetText()
    #if text in contents:
        #start = contents.find(text)
        #range = [start:(start + len(text))]
	#blip.GetDocument().SetAnnotation(range, 'link/manual', url)

    #else:
        pass

def OnBlipSubmitted(properties, context):
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	key = 'chem:'
	endkey = ':'
	if key in contents:
		start = contents.find(key)
		end = contents.find(end, (start + len(key))
		range = [start: end]
		query = contents[(start + len(key): end]
		compound = ChemSpiPy.simplesearch(query)
		url = "http://www.chemspider.com/Chemical-Structure.%s.html" % compound

		insert = query + " (csid:" + compound  +")"
		blip.GetDocument().InsertText(range, insert)

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hello, I'm ChemSpidey, I will convert text of the form ?chem(chemicalName) to a link to ChemSpider")



if __name__ == '__main__':
  ChemSpidey = robot.Robot('cameronneylon-test',
                         image_url='http://www.chemspider.com/ImagesHandler.ashx?id=236',
			 version = '1.1',
                         profile_url='http://www.google.com')
  ChemSpidey.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  ChemSpidey.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)

  ChemSpidey.Run(debug=True)
