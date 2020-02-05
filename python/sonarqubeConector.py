import json
import urllib
import urllib.request
import base64
import sys
from qualityCodeResults import QualityCodeResults
from util import Utils

GET_PROJECT_BY_KEY = "/api/projects/index?key="
#GET_PROJECT_BY_KEY = "/api/projects/search?projects="
GET_METRICS_BY_PROJECT = "/api/measures/component?component="
METRICS_KEY = "metricKeys="


class SonarqubeConector:
    def __init__(self, sonarURL, sonarUser, sonarUserPwd):
        try:
            self.sonarURL = sonarURL
            self.sonarUser = sonarUser
            self.sonarUserPwd = sonarUserPwd
            print ("Sonarqube Connector initialized: SonarURL [", self.sonarURL, "], User [", self.sonarUser, "]")
        except: # catch *all* exceptions
            print ("Error in SonarqubeConector.init: ", e)
            e = sys.exc_info()[0]
        
    def loadProjectIdFromSonar(self, myProjectKey):
        try:
            ### Get ProjectId From SonarQube
            urlGetProjectKeyfromSonar = self.sonarURL + GET_PROJECT_BY_KEY + myProjectKey #+ "\"" 
            print ("SonarQube URL:" + urlGetProjectKeyfromSonar)
            print ("Connecting to SonarQube...")
            print ("Searching projectId by projectKey [" + urlGetProjectKeyfromSonar + "] ...")
      
            req = urllib.request.Request(urlGetProjectKeyfromSonar)
            credentials = ('%s:%s' % (self.sonarUser, self.sonarUserPwd))
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))
            req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
            from urllib.request import urlopen
            #with urlopen(urlGetProjectKeyfromSonar) as response:
            with urlopen(req) as response:
                for line in response:
                    line = line.decode('utf-8')  # Decoding the binary data to text.
                    print(line)
                    dataLine = json.loads(line)
                    projectId = dataLine[0]['id']
                    print (projectId)
                    print ("ProjectId is ", projectId)
                    return projectId
        except ValueError as e:
            print ("Error in SonarqubeConector.loadMetricsFromSonar: ")#, e.reason)
            raise ValueError 
        except Exception as e:
            import traceback
            print('Error in SonarqubeConector.loadMetricsFromSonar. Generic exception: ')
            raise e
#        except: # catch *all* exceptions
#            print ("Error in SonarqubeConector.loadMetricsFromSonar: ")
#            e = sys.exc_info()[0]
#            print ("EXCEPTION in SonarqubeConector.loadMetricsFromSonar. :", e)


    def loadProjectMetricsFromSonar(self, myProjectKey, metricList):
        try:
            print ("loadMetricsFromSonar ... ");
            
            #urlGetMetricsByProject = myprops["sonarURL"] + GET_METRICS_BY_PROJECT + str(projectId) + "&" + METRICS_KEY + metricList
            urlGetMetricsByProject = self.sonarURL + GET_METRICS_BY_PROJECT + myProjectKey + "&" + METRICS_KEY + metricList

            print ("Retrieving Metrics from SonarQube. Metrics to be retrieved [" + metricList + "] ")
            print ("Retrieving Metrics from SonarQube [" + urlGetMetricsByProject + "] ...")
    
            qualityCodeResults = QualityCodeResults()
            
            req = urllib.request.Request(urlGetMetricsByProject)
            credentials = ('%s:%s' % (self.sonarUser, self.sonarUserPwd))
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))
            req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
            from urllib.request import urlopen
            with urlopen(req) as response:
                qualityCodeResults.loadDataFromResponse(response)
            return qualityCodeResults;
            ###sbUri.append(sonarServerIP).append(Constants.GET_METRICS_BY_PROJECT).append(projectKee).append("&")	.append(Constants.METRICS_KEY + metricListString);                      
            
        except ValueError as e:
            print ("Error in SonarqubeConector.loadProjectMetricsFromSonar: ", e)
            raise ValueError 
        except Exception:
            import traceback
            print('Error in SonarqubeConector.loadProjectMetricsFromSonar. Generic exception: ' + traceback.format_exc())
        except: # catch *all* exceptions
            print ("Error in SonarqubeConector.loadProjectMetricsFromSonar: ")
            e = sys.exc_info()[0]
            print ("EXCEPTION in SonarqubeConector.loadProjectMetricsFromSonar. :", e)
        

    def loadDataFromResponse(self, response):
        try:
            for line in response:
                line = line.decode('utf-8')  # Decoding the binary data to text.
                print(line)
        except ValueError as e:
            print ("Error in SonarqubeConector.loadDataFromResponse: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("Error in SonarqubeConector.loadDataFromResponse: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)
