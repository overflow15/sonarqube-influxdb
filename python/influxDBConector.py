import sys
import json
# para instalar la libreria, ejecutar "python3 -m pip install influxdb"
from influxdb import InfluxDBClient
from qualityCodeResults import QualityCodeResults

class InfluxDBConector:
    def __init__(self, influxDBHost, influxDBPort, influxDatabase, influxUser, influxUserPwd):
        try:
            self.influxDBHost = influxDBHost
            self.influxDBPort = influxDBPort
            self.influxDatabase = influxDatabase
            self.influxUser = influxUser
            self.influxUserPwd = influxUserPwd
            print ("InfluxDB Connector initialized: INFLUX URL [", self.influxDBHost, ":", self.influxDBPort, "], InfluxDatabase [", self.influxDatabase, "], User [", self.influxUser, "]")
        except: # catch *all* exceptions
            print ("Error in InfluxDBConector.init: ", e)
            e = sys.exc_info()[0]

    def saveProjectMetrics2InfluxDB(self, metrics):
        try:
            print ("[InfluxDBConectorSaving]: Saving metrics to InfluxDB ... ");
            client = InfluxDBClient(self.influxDBHost, self.influxDBPort, self.influxUser, self.influxUserPwd, self.influxDatabase)
            #client.create_database(self.influxDatabase)
            print("[InfluxDBConectorSaving]: Writing metrics in JSON Format");
            metricsJSONstr = metrics.toJSON()
            print(metricsJSONstr);
            #Convert String to JSON dictionary
            metricsJSON = json.loads(metricsJSONstr)
            print("JSON to be sent to InfluxDB:")
            print(metricsJSON)
            metricsJSON = [metricsJSON, ]
            success = client.write_points(metricsJSON)
            #client.write(metrics.toJSON())
            if success :
                print ("[InfluxDBConectorSaving]: Saved metrics to InfluxDB.")
            else: 
                print ("[InfluxDBConectorSaving]: ERROR saving metrics to InfluxDB.")
            return success
        except Exception as e:
            print ("Error in InfluxDBConector.saveProjectMetrics2InfluxDB: ", e)
        except ValueError as e:
            print ("Error in InfluxDBConector.saveProjectMetrics2InfluxDB: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("Error in InfluxDBConector.saveProjectMetrics2InfluxDB: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)    
    
     
            
        
