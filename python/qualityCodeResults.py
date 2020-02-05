import sys
import json
import datetime

class QualityCodeResults:
    def __init__(self):
        self.projectName = ""
        self.analysysDate = datetime.datetime.now()
        self.sonar_project = 0
        self.comment_lines_density = 0.0
        self.minor_violations = 0
        self.major_violationss = 0
        self.code_smells = 0
        self.bugs = 0
        self.info_violations = 0
        self.files = 0
        self.false_positive_issues = 0
        self.vulnerabilities = 0
        self.lines = 0
        self.ncloc = 0
        self.directories = 0
        self.coverage = 0.0
        self.violations = 0
        self.functions = 0
        self.critical_violations = 0
        self.duplicated_lines_density = 0.0
        self.complexity_in_functions = 0
        self.blocker_violations = 0
        self.score = 0

    # Searchs for the specified metric and returns its value (returns -1 if no found)
    def findValue4Metric(self, json_object, metricName):
        try:
            for dict in json_object:
                if dict['metric'] == metricName:
                    return dict['value']
        except ValueError as e:
            print ("Error in findValue4Metric: ", e)
            raise ValueError
        except: # catch *all* exceptions
            print ("Error in findValue4Metric: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)


    def loadDataFromResponse(self, response):
        try:
#            for line in response:
#                line = line.decode('utf-8')  # Decoding the binary data to text.
#                print(line)

            print("*** Readed Metrics:");
            #jsonResponse = json.loads(response)
            jsonResponse = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
            #print(jsonResponse)
            responseComponent = jsonResponse["component"]
            responseMeasures = responseComponent["measures"]
            self.projectName = responseComponent["name"]
            print(" - projectName: " , self.projectName);
            self.projectKey = responseComponent["key"]
            print(" - projectKey: " , self.projectKey);
            self.analysysDate = datetime.datetime.now()
            print(" - analysysDate: " , self.analysysDate);
            self.sonar_project = 0
            print(" - sonar_project: " , self.sonar_project);
            self.comment_lines_density = float(self.findValue4Metric(responseMeasures, "comment_lines_density"))
            print(" - comment_lines_density: " , float(self.comment_lines_density))
            self.minor_violations = int(self.findValue4Metric(responseMeasures, "minor_violations"))
            print(" - minor_violations: " , self.minor_violations);
            self.major_violations = int(self.findValue4Metric(responseMeasures, "major_violations"))
            print(" - major_violations: " , self.major_violations);
            self.code_smells = int(self.findValue4Metric(responseMeasures, "code_smells"))
            print(" - code_smells: " , self.code_smells);
            self.bugs = int(self.findValue4Metric(responseMeasures, "bugs"))
            print(" - bugs: " , self.bugs);
            self.info_violations = int(self.findValue4Metric(responseMeasures, "info_violations"))
            print(" - info_violations: " , self.info_violations);
            self.files = int(self.findValue4Metric(responseMeasures, "files"))
            print(" - files: " , self.files);
            self.false_positive_issues = int(self.findValue4Metric(responseMeasures, "false_positive_issues"))
            print(" - false_positive_issues: " , self.false_positive_issues);
            self.vulnerabilities = int(self.findValue4Metric(responseMeasures, "vulnerabilities"))
            print(" - vulnerabilities: " , self.vulnerabilities)
            self.lines = int(self.findValue4Metric(responseMeasures, "lines"))
            print(" - lines: " , self.lines)
            self.ncloc = int(self.findValue4Metric(responseMeasures, "ncloc"))
            print(" - ncloc: " , self.ncloc)
            aux = self.findValue4Metric(responseMeasures, "directories")
            if (aux == None ):
                self.directories = 0
            else:
                self.directories = int(aux)
            print(" - directories: [" , self.directories, "]")
            self.coverage = float(self.findValue4Metric(responseMeasures, "coverage"))
            print(" - coverage: " , self.coverage)
            self.violations = int(self.findValue4Metric(responseMeasures, "violations"))
            print(" - violations: " , self.violations)
            self.functions = int(self.findValue4Metric(responseMeasures, "functions"))
            print(" - functions: " , self.functions)
            self.critical_violations = int(self.findValue4Metric(responseMeasures, "critical_violations"))
            print(" - critical_violations: " , self.critical_violations)
            self.duplicated_lines_density = float(self.findValue4Metric(responseMeasures, "duplicated_lines_density"))
            print(" - duplicated_lines_density: " , self.duplicated_lines_density)
            #self.complexity_in_functions = float(self.findValue4Metric(responseMeasures, "complexity_in_functions"))
            print(" - complexity_in_functions: " , self.complexity_in_functions)
            self.blocker_violations = int(self.findValue4Metric(responseMeasures, "blocker_violations"))
            print(" - blocker_violations: " , self.blocker_violations)
            self.score = 0.0
            print(" - score: " , self.score)
            print(" ... ");

        except ValueError as e:
            print ("Error in QualityCodeResults.loadDataFromResponse: ", e)
            raise ValueError
        except: # catch *all* exceptions
            print ("Error in QualityCodeResults.loadDataFromResponse: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)


    def toString(self):
        print("Metrics:");
        print(" - projectName: " , self.projectName)
        print(" - projectKey: " , self.projectKey)
        print(" - analysysDate: " , self.analysysDate)
        print(" - sonar_project: " , self.sonar_project)
        print(" - comment_lines_density: " , self.comment_lines_density)
        print(" - minor_violations: " , self.minor_violations)
        print(" - major_violations: " , self.major_violations)
        print(" - code_smells: " , self.code_smells)
        print(" - bugs: " , self.bugs)
        print(" - info_violations: " , self.info_violations)
        print(" - files: " , self.files)
        print(" - false_positive_issues: " , self.false_positive_issues)
        print(" - vulnerabilities: " , self.vulnerabilities)
        print(" - lines: " , self.lines)
        print(" - ncloc: " , self.ncloc)
        print(" - directories: " , self.directories)
        print(" - coverage: " , self.coverage)
        print(" - violations: " , self.violations)
        print(" - functions: " , self.functions)
        print(" - critical_violations: " , self.critical_violations)
        print(" - duplicated_lines_density: " , self.duplicated_lines_density)
        print(" - complexity_in_functions: " , self.complexity_in_functions)
        print(" - blocker_violations: " , self.blocker_violations)
        print(" - score: " , self.score)
        print(" ... ")

    def toJSON(self):
        myJSON = (''
                      '{'
                           '\"measurement\": \"SonarMetrics\",'
                           '\"tags\": {'
                                '\"project\": \"' + self.projectName + '\",'
                                '\"projectKey\": \"' + self.projectKey + '\"'
                           '},'
                           '\"time\": \"' + self.analysysDate.strftime("%Y-%m-%dT%H:%M:%SZ") + '\"'
                       ','
                           '\"fields\": {'
                                '\"violations\": ' + str(self.violations) + ','
                                '\"comment_lines_density\": ' + str(self.comment_lines_density) + ','
                                '\"minor_violations\": ' + str(self.minor_violations) + ','
                                '\"major_violations\": ' + str(self.major_violations) + ','
                                '\"code_smells\": ' + str(self.code_smells) + ','
                                '\"bugs\": ' + str(self.bugs) + ','
                                '\"info_violations\": ' + str(self.info_violations) + ','
                                '\"files\": ' + str(self.files) + ','
                                '\"false_positive_issues\": ' + str(self.false_positive_issues) + ','
                                '\"vulnerabilities\": ' + str(self.vulnerabilities) + ','
                                '\"lines\": ' + str(self.lines) + ','
                                '\"ncloc\": ' + str(self.ncloc) + ','
                                '\"directories\": ' + str(self.directories) + ','
                                '\"coverage\": ' + str(self.coverage) + ','
                                '\"violations\": ' + str(self.violations) + ','
                                '\"functions\": ' + str(self.functions) + ','
                                '\"critical_violations\": ' + str(self.critical_violations) + ','
                                '\"duplicated_lines_density\": ' + str(self.duplicated_lines_density) + ','
                                '\"complexity_in_functions\": ' + str(self.complexity_in_functions) + ','
                                '\"blocker_violations\": ' + str(self.blocker_violations) + ','
                                '\"score\": ' + str(self.score) + ' '
                            '}'
                        '}'
                   '')
        return myJSON

#'\"time\": \"2009-11-10T23:00:00Z\",'
#self.analysysDate.strftime("%m/%d/%Y, %H:%M:%S")

#metricKeys=
#    lines,
#    ncloc,
#    directories,
#    files,
#    functions,
#    bugs,
#    vulnerabilities,
#    code_smells,
#    comment_lines_density,
#    public_documented_api_density,
#    violations,
#    major_violations,
#    minor_violations,
#    critical_violations,
#    info_violations,
#    blocker_violations,
#    complexity_in_functions,
#    duplicated_lines_density,
#    false_positive_issues,
#    coverage,
#    tests
#{"component":{"id":"AWXtp8wCC4DCXuSp7zeS","key":"com.rcibanque.aba:abaco","name":"ABACO","description":"ABACO Project","qualifier":"TRK",
#"measures":[{"metric":"false_positive_issues","value":"0","periods":[{"index":1,"value":"0"}]},{"metric":"lines","value":"291042","periods":[{"index":1,"value":"4919"}]},{"metric":"directories","value":"460","periods":[{"index":1,"value":"5"}]},{"metric":"coverage","value":"0.0","periods":[{"index":1,"value":"0.0"}]},{"metric":"violations","value":"5307","periods":[{"index":1,"value":"106"}]},{"metric":"blocker_violations","value":"3","periods":[{"index":1,"value":"0"}]},{"metric":"functions","value":"33832","periods":[{"index":1,"value":"451"}]},{"metric":"code_smells","value":"5292","periods":[{"index":1,"value":"107"}]},{"metric":"bugs","value":"15","periods":[{"index":1,"value":"-1"}]},{"metric":"comment_lines_density","value":"11.6","periods":[{"index":1,"value":"-0.09999999999999964"}]},{"metric":"duplicated_lines_density","value":"22.7","periods":[{"index":1,"value":"-0.1999999999999993"}]},{"metric":"major_violations","value":"1701","periods":[{"index":1,"value":"108"}]},{"metric":"ncloc","value":"192480","periods":[{"index":1,"value":"4001"}]},{"metric":"files","value":"2039","periods":[{"index":1,"value":"26"}]},{"metric":"critical_violations","value":"1236","periods":[{"index":1,"value":"19"}]},{"metric":"info_violations","value":"139","periods":[{"index":1,"value":"4"}]},{"metric":"vulnerabilities","value":"0","periods":[{"index":1,"value":"0"}]},{"metric":"complexity_in_functions","value":"42333","periods":[{"index":1,"value":"1545"}]},{"metric":"minor_violations","value":"2228","periods":[{"index":1,"value":"-25"}]}]}}
