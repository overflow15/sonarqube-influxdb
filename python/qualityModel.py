import sys

#	public static final double MINIMUM_SCORE = 0.0;
#	public static final double MAXIMUM_SCORE = 5.0;
#	public static final double NORMALIZED_SCORE = 1.0;
#	public static final double MAX_PERCENTAGE = 100.0;



class QualityModel:
  def __init__(self, qualityModelFilename):
    self.qualityModelFilename = qualityModelFilename
    #self.max_violations_rate = 0
    
    try:
        # Read quality model properties configuration file
        myQualityModel = {}
        with open(qualityModelFilename) as fileobj:
            for line in fileobj:
                if line.find("=") > 0:
                    key, value = line.strip().split("=")
                    myQualityModel[key] = value   
    
        # Assign read values to object atributes
        self.max_violations_rate = float(myQualityModel["max.violations.rate"])
        self.min_violations_rate = float(myQualityModel["min.violations.rate"])
        self.violations_weight = float(myQualityModel["violations.weight"])
        self.violations_penalty = float(myQualityModel["violations.penalty"])
        self.violations_bonus = float(myQualityModel["violations.bonus"])
        ###severity.factors=1.0,1.8,2.4,5.0,10.0
        severity_factorsStr = myQualityModel["severity.factors"].split(',')
        self.severity_factors = [float(i) for i in severity_factorsStr]
        #for x in range(5):
        #    print("severity.factors [" ,x, "]:", self.severity_factors[x])
        
        self.coverage_min_value = float(myQualityModel["coverage.min.value"])
        self.coverage_max_value = float(myQualityModel["coverage.max.value"])
        self.coverage_bonus = float(myQualityModel["coverage.bonus"])
        self.coverage_penalty = float(myQualityModel["coverage.penalty"])
        self.coverage_weight = float(myQualityModel["coverage.weight"])
        coverage_levelsStr = myQualityModel["coverage.levels"].split(',') ###coverage.levels=11.0,22.0,45.0,65.0,85.0
        self.coverage_levels = [float(i) for i in coverage_levelsStr]
        complexity_levelsStr = myQualityModel["complexity.levels"].split(',') ###complexity.levels=21.0,12.5,9.2,4.5,2.0
        self.complexity_levels = [float(i) for i in complexity_levelsStr]
        self.complexity_min_value = float(myQualityModel["complexity.min.value"])
        self.complexity_max_value = float(myQualityModel["complexity.max.value"])
        self.complexity_bonus = float(myQualityModel["complexity.bonus"])
        self.complexity_penalty = float(myQualityModel["complexity.penalty"])
        self.complexity_weight = float(myQualityModel["complexity.weight"])
        comments_levelsStr = myQualityModel["comments.levels"].split(',')  ###comments.levels=2.0,6.0,10.0,15.0,20.0
        self.comments_levels = [float(i) for i in comments_levelsStr]
        self.comments_min_value = float(myQualityModel["comments.min.value"])
        self.comments_max_value = float(myQualityModel["comments.max.value"])
        self.comments_bonus = float(myQualityModel["comments.bonus"])
        self.comments_penalty = float(myQualityModel["comments.penalty"])
        self.comments_weight = float(myQualityModel["comments.weight"])
        # Reverse values for negative high value metric
        duplication_levelsStr = myQualityModel["duplication.levels"].split(',')   ###duplication.levels=30.0,20.0,14.0,7.0,2.0
        self.duplication_levels = [float(i) for i in duplication_levelsStr]
        self.duplication_min_value = float(myQualityModel["duplication.min.value"])
        self.duplication_max_value = float(myQualityModel["duplication.max.value"])
        self.duplication_bonus = float(myQualityModel["duplication.bonus"])
        self.duplication_penalty = float(myQualityModel["duplication.penalty"])
        self.duplication_weight = float(myQualityModel["duplication.weight"])
        #print ("Read max_violations_rate:", self.max_violations_rate)
    
    except ValueError as e:
        print ("Error in QualityModel while reading model properties configuration file: ", e)
        raise ValueError 
    except Exception as e:
        print ("Error in QualityModel while reading model properties configuration file: ", e)
        raise Exception 
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print ("EXCEPTION:", e)
  