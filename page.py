#!/usr/bin/python
"""
Google AJAX Search Module
http://code.google.com/apis/ajaxsearch/documentation/reference.html
"""
try:
    import simplejson as json
except:
    import json
import urllib

URL = 'http://ajax.googleapis.com/ajax/services/search/web?'

#Web Search Specific Arguments
#http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_web
#SAFE,FILTER
"""
SAFE
This optional argument supplies the search safety level which may be one of:
    * safe=active - enables the highest level of safe search filtering
    * safe=moderate - enables moderate safe search filtering (default)
    * safe=off - disables safe search filtering
"""
SAFE_ACTIVE     = "active"
SAFE_MODERATE   = "moderate"
SAFE_OFF        = "off"

"""
FILTER
This optional argument controls turning on or off the duplicate content filter:

    * filter=0 - Turns off the duplicate content filter
    * filter=1 - Turns on the duplicate content filter (default)

"""
FILTER_OFF  = 0
FILTER_ON   = 1

#Standard URL Arguments
#http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_args
"""
RSZ
This optional argument supplies the number of results that the application would like to receive. 
A value of small indicates a small result set size or 4 results. 
A value of large indicates a large result set or 8 results. If this argument is not supplied, a value of small is assumed. 
"""
RSZ_SMALL = "small"
RSZ_LARGE = "large"

"""
HL
This optional argument supplies the host language of the application making the request. 
If this argument is not present then the system will choose a value based on the value of the Accept-Language http header. 
If this header is not present, a value of en is assumed.
"""

class pygoogle2:
    
    def __init__(self, query, site="google.com", pages=13,hl='en'):
        self.pages = pages           #Number of pages. default 13
        self.query = query           #query string, keywords
        self.url_found = 'none'      #url found from search, default='none'
        self.site = site             #site name. default "google.com"
        self.filter = FILTER_ON      #Controls turning on or off the duplicate content filter. On = 1.
        self.rsz = RSZ_LARGE         #Results per page. small = 4 /large = 8
        self.safe = SAFE_OFF         #SafeBrowsing -  active/moderate/off
        self.hl = hl                 #Defaults to English (en)
        self.found_it = False        #if query is successful, it will be set to True
        self.ranking = -1            #if found, the will get the rank
        #print "self.site=%s self.query=%s"%(self.site, self.query)
        
    def __search__(self,print_results = False):
        results = []
        for page in range(0,self.pages):
            rsz = 8
            if self.rsz == RSZ_SMALL:
                rsz = 4
            args = {'q' : self.query,
                    'v' : '1.0',
                    'start' : page*rsz,
                    'rsz': self.rsz,
                    'safe' : self.safe, 
                    'filter' : self.filter,    
                    'hl'    : self.hl
                    }
            q = urllib.urlencode(args)			
            
            search_results = urllib.urlopen(URL+q)
            data = json.loads(search_results.read())

            item_count = 0   # rank of the result 
            page_count = page + 1  # 'cause page starts from 0 
            if print_results:
                if data['responseStatus'] == 200:
                    for result in  data['responseData']['results']:
                        if result:
                            item_count += 1
                            #print '[%s]'%(urllib.unquote(result['titleNoFormatting']))
                            #print result['content'].strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("'","'").strip()
                            #print urllib.unquote(result['unescapedUrl'])+'\n' 
                            
                            # found!! 							
                            if result['unescapedUrl'].find(site) != -1:
                                self.ranking = page*rsz + item_count
                                print "Found!!!!!! ranking = %s" %(self.ranking)
                                self.found_it = True

                        if self.found_it == True: 
                            self.url_found = result['unescapedUrl']
                            print "***url_found=%s" %(self.url_found)
                            break						
							
            results.append(data)
            if self.found_it == True:
                break;
        return results
    
    def search(self):
        """Returns a dict of Title/URLs"""
        print "Returns a dict of Title/URLs"
        results = {}
        for data in self.__search__():
            for result in  data['responseData']['results']:
                if result:
                    title = urllib.unquote(result['titleNoFormatting'])
                    results[title] = urllib.unquote(result['unescapedUrl'])
        return results

    def search_page_wise(self):
        """Returns a dict of page-wise urls"""
        results = {}
        for page in range(0,self.pages):
            args = {'q' : self.query,
                    'v' : '1.0',
                    'start' : page,
                    'rsz': RSZ_LARGE,
                    'safe' : SAFE_OFF, 
                    'filter' : FILTER_ON,    
                    }
            q = urllib.urlencode(args)
            search_results = urllib.urlopen(URL+q)
            data = json.loads(search_results.read())
            urls = []
            for result in  data['responseData']['results']:
                if result:
                    url = urllib.unquote(result['unescapedUrl'])
                    urls.append(url)            
            results[page] = urls
        return results
        
    def get_urls(self):
        """Returns list of result URLs"""
        results = []
        for data in self.__search__():
            for result in  data['responseData']['results']:
                if result:
                    results.append(urllib.unquote(result['unescapedUrl']))
        return results

    def get_result_count(self):
        """Returns the number of results"""
        print "Returns the number of results"
        temp = self.pages
        #self.pages = 1
        result_count = 0
        try:
            result_count = self.__search__(True)[0]['responseData']['cursor']['estimatedResultCount']
        except Exception,e:
            print e
        finally:
            self.pages = temp
        return result_count	
        
    def display_results(self):
        """Prints results (for command line)"""
        self.__search__(True)

"""
Sample command : 
    python page.py stackoverflow.com multithreading
     
Sample output: rank url 
    10 http://stackoverflow.com/questions/tagged/multithreading
"""

if __name__ == "__main__":
    import sys
    site = sys.argv[1]
    query = ' '.join(sys.argv[2:])
    print "query=%s"%(query)
    g = pygoogle2(query, site)
    print '*Found %s results*'%(g.get_result_count())

    # This is the output 
    print g.url_found, g.ranking

    #g.display_results()
