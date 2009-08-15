import urllib
from xml.etree import cElementTree as ET


class ChemSpiderId(str):
    """An class for holding ChemSpider IDs and enabling searches based on them.

    The purpose of the class is to enable a series of bound methods to be easily
    wrapped to provide access to the ChemSpider API in Python. Currently the 
    methods include returning the URL of a png image of the named chemical.
    """

    def __init__(self,csid):
        """Initialize the ChemSpiderId object with a value.

        """

        self.id = ""

        if type(csid) == str and csid.isdigit() == True:
            self.id = csid
            
        elif type(csid) == int:
            self.id = str(csid)

        else:
            raise TypeError('ChemSpiderId needs to be intialised with an int or a str')

    def __string__(self):
        return self.id

    def imageurl(self):
        """ Return the URL of a png image for a specific Chemspider ID.

        The actual ChemSpider API returns the binary of the PNG wrapped in XML. The
        purpose of constructing a URL to the image is to enable easy insertion into
        webservices etc by serving the address for the image rather than the image.
        """

        assert self != '', 'ChemSpiderId not initialised with value'

        baseurl = 'http://www.chemspider.com/'
        url = baseurl + 'ImagesHandler.ashx?id=%s' % self
        return url


def simplesearch(query):
    """Returns ChemSpiderId string from a simple search for query.

    SimpleSearch on the Chempspider API provides a list of objects which this
    routine is currently capturing but not returning back. At the moment it 
    simply returns a single object of the type ChemSpiderID
    """

    assert type(query) == str, 'query not a string object'

    baseurl = 'http://www.chemspider.com/'
    token  = '3a19d00d-874f-4879-adc0-3013dbecbbc9'

    # Construct a search URL and poll Chemspider for the XML result
    searchurl = baseurl + 'Search.asmx/SimpleSearch?query=' + query + '&token=' + token

    response = urllib.urlopen(searchurl)

    tree = ET.parse(response) #parse the CS XML response
    elem = tree.getroot()
    csid_tags = elem.getiterator('{http://www.chemspider.com/}int')

    csidlist = []
    for tags in csid_tags:
      csidlist.append(tags.text)
    
    returned_id = ChemSpiderId(csidlist[0])

    return returned_id

########################################
#
# Unit tests
#
########################################

