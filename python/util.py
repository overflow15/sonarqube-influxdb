import sys

class Utils(object):
    def loadPropertiesFile(myPropertiesFilename):
        myprops = {}
        try:
            print ("Reading properties file: ", myPropertiesFilename, "...")
            with open(myPropertiesFilename) as fileobj:
                for line in fileobj:
                    if line.find("=") > 0:
                        key, value = line.strip().split("=")
                        #Quitar espacios
                        key=key.replace(' ', '')
                        value=value.replace(' ', '')
                        myprops[key] = value   
        except ValueError as e:
            print ("Fatal Error While reading Properties File: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)
        return myprops
 