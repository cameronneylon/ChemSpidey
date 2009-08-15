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


def OnBlipSubmitted(properties, context):
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	if '?chem' in contents:
		query = '"%s"' % contents.replace('?chem', '').replace('"', ' ').replace('\n', '')
		compound = ChemSpiPy.simplesearch(query)
		url = "http://www.chemspider.com/Chemical-Structure.%s.html" % compound
		content = query + "(" + url +")"
		blip.GetDocument().SetText(content)



if __name__ == '__main__':
  ChemSpidey = robot.Robot('chemspidey',
                         image_url='http://www.chemspider.com/ImagesHandler.ashx?id=236',
                         profile_url='http://www.google.com')
  ChemSpidey.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  ChemSpidey.Run(debug=True)
