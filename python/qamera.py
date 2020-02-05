import json
import urllib
import urllib.request
import sys
from util import Utils
from qualityModel import QualityModel
from sonarqubeConector import SonarqubeConector
from qualityCodeResults import QualityCodeResults
from influxDBConector import InfluxDBConector
from qualityRateEvaluator import QualityRateEvaluator

print("Starting QAmera....")

# Read properties file
try:
    print("INICIO...")
    
    ##################################################################################################
    # Comprobar numero argumentos
    #     EJEMPLO: python qamera.py application.properties com.rcibanque.aba:abaco
    ##################################################################################################
    if len(sys.argv) <= 2 :
        print ("ERROR: Numero de parametros erroneo. Debe invocarse de este modo:")
        print ("    Arg1: fichero de propiedades (application.properties)")
        print ("    Arg2: ProjectKey en SonarQube correspondiente al elemento a analizar")
        sys.exit(0)
    
    #myPropertiesFile = "D://Alfonso//AAProyectos//qamera_python//application.properties"
    myPropertiesFile = sys.argv[1]
    myProjectKey = sys.argv[2]
    print ("Parametros de ejecucion:")
    print ("Fichero de propiedades:", myPropertiesFile)
    print ("Parametros de ejecucion:", myProjectKey)
    print ("...")
    
    ### Read Program Properties from configuration file
    myprops = {}
    myprops = Utils.loadPropertiesFile(myPropertiesFile)

    ### Read Quality Model from configuration file
    myQualityModel = QualityModel(myPropertiesFile)
    print("Quality Model:", myQualityModel.max_violations_rate)
       
    ### Connecto to SonarQube
    mySonarqubeConector = SonarqubeConector(myprops["sonarURL"], myprops["sonarUser"], myprops["sonarCredentials"])
    ### Get ProjectId From SonarQube
    myProjectId = mySonarqubeConector.loadProjectIdFromSonar(myProjectKey)
    ### Get Metrics from SonarQube
    metricList =  myprops["metrics"]
    qualityCodeResults = mySonarqubeConector.loadProjectMetricsFromSonar(myProjectKey, metricList)
    print ("Quality Code results received from SonarQube:")
    print (qualityCodeResults.toString())
    
    ### Calculate QA Score (using defined qality model)
    QualityRateEvaluator.evaluate(qualityCodeResults,myQualityModel) 
    print("Calculated Quality Score:", qualityCodeResults.score)
    
    ### Save results in influxDB
    print("Creating InfluxDB Connection ...")
    myInfluxDBConector = InfluxDBConector(myprops["influxDB_Host"], myprops["influxDB_Port"], myprops["influxDB_Database"], myprops["influxDB_User"], myprops["influxDB_UserPwd"])
    print("Saving results to InfluxDB ...")
    if myInfluxDBConector.saveProjectMetrics2InfluxDB(qualityCodeResults):
         print("Results Successfully saved to InfluxDB.")
    else: 
         print("An ERROR ocurred trying to save results to InfluxDB.")
    print("Ending ...");

except Exception as e:
    print ("Excepcion no capturada")
    raise e  
        
#except: # catch *all* exceptions
    #e = sys.exc_info()[0]
    #print ("EXCEPTION:", e)



