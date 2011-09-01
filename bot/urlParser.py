import re
import sys
import Image
import urllib2
import mimetypes
from tld import TLD

#link is the actual link/url
#ltype is the type of link it is (http, direct connect, ftp, etc)
#uname is the username if there is one for ftp, http, connections
#ptld is the TLD (.co.uk, .com, etc)
#ip is the ip address if any
#pathres if the path after the domain www.blah.com/this/blah.txt has /this/blah.txt
#gftype is the mime type (jpeg, mpeg, etc)
#domain is the domain including tld
#port if there is one after domain:
def parse(message):
    prog = re.compile("(?P<link>(?:(?P<ltype>[a-z0-9]{2,15})\:\/\/)?(?:(?P<uname>[-_\w]+)\:?\w*@)?(?:(?P<domain>[\.\-_\w]*\.(?P<ptld>[a-z]{2,}))|(?P<ip>(?:(?:[01]?[0-9]{1,2}|2(?:[0-4][0-9]|5[0-5]))\.){3}(?:[01]?[0-9]{1,2}|2(?:[0-4][0-9]|5[0-5]))))(?:\:(?P<port>\d+))?\/?(?P<pathres>[\w\#\/\Q~:;,.?+=&%@!-\E]+)?)",re.I)
    result = prog.search(message)
    if result is None:
        return "No regexp match"
    
    link = result.group('link')
    #If the link is None, return None
    if link is None:
        return "No link in message"
    
    ltype = result.group('ltype')
    uname = result.group('uname')
    domain = result.group('domain')
    ptld = result.group('ptld')
    ip = result.group('ip')
    pathres = result.group('pathres')
    #Try and convert the port to an int
    try:
        port = int(result.group('port'))
    except (ValueError, TypeError):
        port = None
    
    #validate the TLD including if the TLD is actually real
    variable = TLD()
    istld = variable.Validate(ptld)
    if(not istld):
        #the tld isn't valid, return non
        return "Invalid TLD %s" % ptld
    
    #Is there a www at any point
    valwww = link.find('www') > -1
    
    #Determine if the domain of the type xx.yy yy is the tld
    valdomain = re.search("\w+.\w+$",domain)
    
    #try and find the type of file it is text/plain etc
    gftype = mimetypes.guess_type(link)[0]
    
    #Determine if an ip is present
    isip = not (ip is None)
    
    
    #If there's no ltype (ftp:// http:// etc)
    if ltype is None:
        #If there's no tld, ip, port, www but there is a mime type then it's a file
        if not istld and port is None and not isip and not valwww and gftype is not None:
            #This is a file, return null
            return "File"
        elif not isip and not valwww and pathres is None and not port is None and istld and uname is not None:
            #An email, return null
            return "Email"
        elif (isip or (valdomain and istld)) and not valwww:
            ltype = 'dcon'
            #Direct connection, try it out
        #No ltype, ip, port or www value
        elif not isip and port is None and not valwww:
            #Unknown format, return null
            return "Unknown"
    
    if (((valdomain and istld) or isip) and (ltype == 'http' or (ltype is None and valwww) or ltype == 'dcon')):
            #Look at using http://www.crummy.com/software/BeautifulSoup/
        try:
            #Save the proper url for later use
            tlink = link
    
            #If the url doesn't start with http://, make it so
            link = link if link.find('http://') != -1 else 'http://' + link
            sys.stdout.write("Querying: %s" % link)
            page = urllib2.urlopen(link)
            content_type = None
            content_len  = None
    
            #Get the content-type and content-length headers
            for header in page.info().headers: 
                if header[:header.find(':')].lower() == 'content-type': 
                    content_type = header[header.find(':')+1:].strip()
                elif header[:header.find(':')].lower() == 'content-length': 
                    content_len =  header[header.find(':')+1:].strip()
    
            if content_len is None:
                #If there is no content we cannot continue
                return "No Content Length"
            if content_type is None:        
                #If there is no type it's malformed
                return "No Content Type"
    
            if(re.search("text|(?:application.*xml)",content_type,re.I)):
                #Read the page and get the title
                pagedata = page.read()
                title = re.search("(?<=<title>).*(?=</title>)",pagedata.translate(None,"\t\n\r"), re.IGNORECASE)
    
                #Get the title
                dtitle = title.group(0)
                #Strip non valid characters and white spaces greater than 2 long
                dtitle = re.sub('[^\[\]\w\s,._\-\/\\}{]+', '', dtitle)
                dtitle = re.sub('/\s{2,}', '', dtitle);
    
                #If the title still has content use it, otherwise, use the url
                title = dtitle if len(dtitle) != 0 else turl;
                return "Insert into links"
            elif(re.search("image\/",content_type, re.I)):
                findex = link.rfind('/')
                if(findex == -1):
                   sys.exit(0) 
                fname = link[findex+1:]
                src = re.sub('%20', '', fname)
                dst = '/home/weigonchi/img/thumb/'+re.sub('(?P<grp>.*)\.(?:\w+)$','\g<grp>.png', fname, re.I)
                src = '/home/weigonchi/img/'+fname
    
                ## Open our local file for writing
                #local_file = open(src, "w")
                ##Write to our local file
                #local_file.write(page.read())
                #local_file.close()
    
                #img = Image.open(src)
                #img.thumbnail((128, 102), Image.ANTIALIAS)
                #img.save(dst)
                return "%s to %s" % (src, dst)
                
    
    
        except Exception as exc:
            #Deal with HTTPError as per http://www.voidspace.org.uk/python/articles/urllib2.shtml#handling-exceptions
            print exc
            pass

        #$inserter = $dbh->prepare("INSERT INTO linkage (nick, whence, link, channel, pgTitle, pgType, pgSize, ltype,pgfType,imgCached,imgThumb) VALUES (?,now(),?,?,?,?,?,?,?,?,?)");
iurl = raw_input('URL: ')
sys.stdout.write(parse(iurl))
sys.stdout.write('\n')