####################################################################################################
# Modelo de calidad (reglas de cálculo)
# Se evaluan estas característicascde calidad:
#     - Violations (incumplimientos).- se multiplica el número de incumplomientos por un factor que depende de su severidad (blocker, critical, major, minor, info)
#           Notas:
#            + La nota se trunca a 2/5 del máximo posible si hay alguna violación Blocker o Critical
#     - Coverage.- cobertura tests unitarios. Cuanto más mejor
#     - Densidad de comentarios.- cuanto más mejor
#     - COmplexity.- cuanto menos mejor
#     - Duplications.- cuanto menos mejor
# A cada característica se le da un peso en el fichero properties (weight), y la suma de los pesos debe ser la nota máxima MAX_RATE = 5
     
#
####################################################################################################
import sys
import json
import datetime

MAX_SCORE = 5.0
MIN_SCORE = 0.0


class QualityRateEvaluator:
    
    def evaluate(qualityCodeResults, myQualityModel):
        try:
            print ("Evaluating Quality Code Metrics ...")
            totalRate = QualityRateEvaluator.calculateViolationsRate(qualityCodeResults, myQualityModel)
            totalRate += QualityRateEvaluator.calculateDuplicationsRate(qualityCodeResults, myQualityModel)
            totalRate += QualityRateEvaluator.calculateCommentsRate(qualityCodeResults, myQualityModel)
            totalRate += QualityRateEvaluator.calculateCoverageRate(qualityCodeResults, myQualityModel)
            totalRate += QualityRateEvaluator.calculateComplexityRate(qualityCodeResults, myQualityModel)
            
            qualityCodeResults.score = totalRate
        except Exception as e:
            print ("Error in QualityRateEvaluator.evaluate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.evaluate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)



    def calculateViolationsRate(qualityCodeResults, myQualityModel):
        try:
            aggregatedMetricsWeight = myQualityModel.violations_weight + myQualityModel.coverage_weight + myQualityModel.duplication_weight + myQualityModel.complexity_weight + myQualityModel.comments_weight 
            violationsScore = MIN_SCORE
            print ("  Evaluating Violations...")
            print ("    Evaluating Blocker Violations Metric. Num violations:", qualityCodeResults.blocker_violations, ". Severity Factor: ", myQualityModel.severity_factors[4])
            blockerViolationsFactor =  qualityCodeResults.blocker_violations * myQualityModel.severity_factors[4]
            print ("    Blocker Violations Metric:", blockerViolationsFactor)

            print ("    Evaluating Critical Violations Metric. Num violations:", qualityCodeResults.critical_violations, ". Severity Factor: ", myQualityModel.severity_factors[3])
            criticalViolationsFactor =  qualityCodeResults.critical_violations * myQualityModel.severity_factors[3]
            print ("    Critical Violations Metric:", criticalViolationsFactor)

            print ("    Evaluating Major Violations Metric. Num violations:", qualityCodeResults.major_violations, ". Severity Factor: ", myQualityModel.severity_factors[2])
            majorViolationsFactor =  qualityCodeResults.major_violations * myQualityModel.severity_factors[2]
            print ("    Major Violations Metric:", majorViolationsFactor)

            print ("    Evaluating Minor Violations Metric. Num violations:", qualityCodeResults.minor_violations, ". Severity Factor: ", myQualityModel.severity_factors[1])
            minorViolationsFactor =  qualityCodeResults.minor_violations * myQualityModel.severity_factors[1]
            print ("    Minor Violations Metric:", minorViolationsFactor)

            print ("    Evaluating Info Violations Metric. Num violations:", qualityCodeResults.info_violations, ". Severity Factor: ", myQualityModel.severity_factors[0])
            infoViolationsFactor =  qualityCodeResults.info_violations * myQualityModel.severity_factors[0]
            print ("    Info Violations Metric:", infoViolationsFactor)

            totalViolationsFactor = blockerViolationsFactor + criticalViolationsFactor + majorViolationsFactor + minorViolationsFactor + infoViolationsFactor
            print ("    Total Violations Metric:", totalViolationsFactor)
            
            print ("    NCLOC:", qualityCodeResults.ncloc, ". Violations Metric:", totalViolationsFactor)
            violationsRate = qualityCodeResults.ncloc / totalViolationsFactor
            print ("    Violations Rate [NCLOC / totalViolationsMetric] (higher is better):", violationsRate)
            
            if violationsRate > myQualityModel.max_violations_rate:
                violationsScore = MAX_SCORE
                print ("    Violations Rate is higher than MAX value (very good!). Set violationsScore to:", violationsScore)
            elif violationsRate < myQualityModel.min_violations_rate:
                violationsScore = MIN_SCORE
                print ("    Violations Rate is lower than MIN value (very bad!). Set violationsScore to:", violationsScore)
            else:
                # Calculate 3 rule
                violationsScore = (MAX_SCORE * (violationsRate - myQualityModel.min_violations_rate)) / (myQualityModel.max_violations_rate - myQualityModel.min_violations_rate) 
                print (  "    Violations [ ", MIN_SCORE, " - ", MAX_SCORE, " ] Score:", violationsScore)
            
            # If there are blocker or critical violations, absolute score is truncated to 2 point over 5
            truncatedScore = 2 * (MAX_SCORE / 5)  
            if ((violationsScore > truncatedScore) and (qualityCodeResults.blocker_violations + qualityCodeResults.critical_violations > 0)):
                violationsScore = truncatedScore
                print ("    Violations Score truncated due to blocker / critical violations:", violationsScore)


            violationsWeightedScore = (violationsScore * myQualityModel.violations_weight) / aggregatedMetricsWeight
            
            # If Score is higher than MAX, apply a BONUS
            if violationsScore >= MAX_SCORE:
                violationsWeightedScore += myQualityModel.violations_bonus;
                print ("    Reached Max Violations Metric Score --> BONUS [+", myQualityModel.violations_bonus, "] applied.") 
            # If Score is lower than MAX, apply a PENALTY
            if violationsScore <= MIN_SCORE:
                violationsWeightedScore -= myQualityModel.violations_penalty;
                print ("    Violations score is too low --> PENALTY [-", myQualityModel.violations_penalty, "] applied.") 

            print ("    Violations Metric Weight is ", myQualityModel.violations_weight , " and violations Score is ",  violationsScore)
            print ("  Final Violations Rated score (Weighted) is: ", violationsWeightedScore)
            print ("  ")
            return violationsWeightedScore    
        except Exception as e:
            print ("Error in QualityRateEvaluator.calculateViolationsRate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.calculateViolationsRate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)

    def calculateCommentsRate(qualityCodeResults, myQualityModel):
        try:
            aggregatedMetricsWeight = myQualityModel.violations_weight + myQualityModel.coverage_weight + myQualityModel.duplication_weight + myQualityModel.complexity_weight + myQualityModel.comments_weight 
            score = MIN_SCORE
            weightedScore = MIN_SCORE
            print ("  Evaluating Comments density rate...")
            print ("    Comments density percent (SonarMetric): ", qualityCodeResults.comment_lines_density)
            
            if qualityCodeResults.comment_lines_density < myQualityModel.comments_levels[0]:
                score = MIN_SCORE
                print ("    Metric is lower than Score Level 1 (very bad!). Set Score to:", MIN_SCORE)
            elif qualityCodeResults.comment_lines_density > myQualityModel.comments_levels[4]:
                score = MAX_SCORE
                print ("    Metric is higher than Score Level 5 (very good!). Set Score to:", MAX_SCORE)
            else:
                level = 1
                while ((level < 5) & (qualityCodeResults.comment_lines_density > myQualityModel.comments_levels[level])):
                    level += 1
                # Reached Score is 1 point for each level reched plus a percentage of the current level (3-rule)
                partialScore = (qualityCodeResults.comment_lines_density - myQualityModel.comments_levels[level-1]) / (myQualityModel.comments_levels[level] - myQualityModel.comments_levels[level-1])
                score = level - 1 + partialScore 
                print ("    Value is between Score Level ", level-1, " (", myQualityModel.comments_levels[level-1], ") and ", level, " (", myQualityModel.comments_levels[level], "). Set Score to:", score)
            
            weightedScore = (score * myQualityModel.comments_weight) / aggregatedMetricsWeight
            
            # If Score is higher than MAX, apply a BONUS
            if qualityCodeResults.comment_lines_density > myQualityModel.comments_max_value:
                weightedScore += myQualityModel.comments_bonus;
                print ("    Score is higher than MAX --> BONUS [+", myQualityModel.comments_bonus, "] applied.") 
            # If Score is lower than MIN, apply a PENALTY
            if qualityCodeResults.comment_lines_density < myQualityModel.comments_min_value:
                weightedScore -= myQualityModel.comments_penalty;
                print ("    Score is too low --> PENALTY [-", myQualityModel.comments_penalty, "] applied.") 

            print ("    Comments Density Metric Weight is ", myQualityModel.comments_weight , " and Score is ",  score)
            print ("  Final Comments Density Rated score (Weighted) is: ", weightedScore)
            print ("  ")            
            return weightedScore
            
        except Exception as e:
            print ("Error in QualityRateEvaluator.calculateCommentsRate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.calculateCommentsRate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)


    def calculateCoverageRate(qualityCodeResults, myQualityModel):
        try:
            aggregatedMetricsWeight = myQualityModel.violations_weight + myQualityModel.coverage_weight + myQualityModel.duplication_weight + myQualityModel.complexity_weight + myQualityModel.comments_weight 
            score = MIN_SCORE
            weightedScore = MIN_SCORE
            print ("  Evaluating Test Coverage rate...")
            print ("    Test Coverage percent (SonarMetric): ", qualityCodeResults.coverage)
            
            if qualityCodeResults.coverage < myQualityModel.coverage_levels[0]:
                score = MIN_SCORE
                print ("    Metric is lower than Score Level 1 (very bad!). Set Score to:", MIN_SCORE)
            elif qualityCodeResults.coverage > myQualityModel.coverage_levels[4]:
                score = MAX_SCORE
                print ("    Metric is higher than Score Level 5 (very good!). Set Score to:", MAX_SCORE)
            else:
                level = 1
                while ((level < 5) & (qualityCodeResults.coverage > myQualityModel.coverage_levels[level])):
                    level += 1
                # Reached Score is 1 point for each level reched plus a percentage of the current level (3-rule)
                partialScore = (qualityCodeResults.coverage - myQualityModel.coverage_levels[level-1]) / (myQualityModel.coverage_levels[level] - myQualityModel.coverage_levels[level-1])
                score = level - 1 + partialScore 
                print ("    Value is between Score Level ", level-1, " (", myQualityModel.coverage_levels[level-1], ") and ", level, " (", myQualityModel.coverage_levels[level], "). Set Score to:", score)
            
            weightedScore = (score * myQualityModel.coverage_weight) / aggregatedMetricsWeight
            
            # If Score is higher than MAX, apply a BONUS
            if qualityCodeResults.coverage > myQualityModel.coverage_max_value:
                weightedScore += myQualityModel.coverage_bonus;
                print ("    Score is higher than MAX --> BONUS [+", myQualityModel.coverage_bonus, "] applied.") 
            # If Score is lower than MIN, apply a PENALTY
            if qualityCodeResults.coverage < myQualityModel.coverage_min_value:
                weightedScore -= myQualityModel.coverage_penalty;
                print ("    Score is too low --> PENALTY [-", myQualityModel.coverage_penalty, "] applied.") 

            print ("    Test Coverage Metric Weight is ", myQualityModel.coverage_weight , " and Score is ",  score)
            print ("  Final Test Coverage Rated score (Weighted) is: ", weightedScore)
            print ("  ")            
            return weightedScore
            
        except Exception as e:
            print ("Error in QualityRateEvaluator.calculateCoverageRate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.calculateCoverageRate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)



    def calculateDuplicationsRate(qualityCodeResults, myQualityModel):
        try:
            aggregatedMetricsWeight = myQualityModel.violations_weight + myQualityModel.coverage_weight + myQualityModel.duplication_weight + myQualityModel.complexity_weight + myQualityModel.comments_weight 
            duplicationScore = MIN_SCORE
            duplicationWeightedScore = MIN_SCORE
            print ("  Evaluating Duplicated Code rate...")
            print ("    Duplications metric (SonarMetric): ", qualityCodeResults.duplicated_lines_density)
            
            # This is a NEGATIVE METRIC: HIHGER IS WORSE
            if qualityCodeResults.duplicated_lines_density > myQualityModel.duplication_levels[0]:
                score = MIN_SCORE
                print ("    Metric is higher than Score Level 1 (very bad!). Set Score to:", MIN_SCORE)
            elif qualityCodeResults.duplicated_lines_density < myQualityModel.duplication_levels[4]:
                score = MAX_SCORE
                print ("    Metric is lower than Score Level 5 (very good!). Set Score to:", MAX_SCORE)
            else:
                level = 1
                while ((level < 5) & (qualityCodeResults.duplicated_lines_density < myQualityModel.duplication_levels[level])):
                    level += 1
                # Reached Score is 1 point for each level reched plus a percentage of the current level (3-rule)
                partialScore = (myQualityModel.duplication_levels[level-1] - qualityCodeResults.duplicated_lines_density) / (myQualityModel.duplication_levels[level-1] - myQualityModel.duplication_levels[level])
                score = level - 1 + partialScore 
                print ("    Value is between Score Level ", level-1, " (", myQualityModel.duplication_levels[level-1], ") and ", level, " (", myQualityModel.duplication_levels[level], "). Set Score to:", score)
            
            weightedScore = (score * myQualityModel.duplication_weight) / aggregatedMetricsWeight
            
            # If Score is higher than MAX, apply a BONUS
            if qualityCodeResults.duplicated_lines_density < myQualityModel.duplication_min_value:
                weightedScore += myQualityModel.duplication_bonus;
                print ("    Score is higher than MAX --> BONUS [+", myQualityModel.duplication_bonus, "] applied.") 
            # If Score is lower than MIN, apply a PENALTY
            if qualityCodeResults.duplicated_lines_density > myQualityModel.duplication_max_value:
                weightedScore -= myQualityModel.duplication_penalty;
                print ("    Score is too low --> PENALTY [-", myQualityModel.duplication_penalty, "] applied.") 

            print ("    Duplicated Code Metric Weight is ", myQualityModel.duplication_weight , " and Score is ",  score)
            print ("  Final Duplicated Code Rated score (Weighted) is: ", weightedScore)
            print ("  ")            
            return weightedScore
            
        except Exception as e:
            print ("Error in QualityRateEvaluator.calculateDuplicationsRate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.calculateDuplicationsRate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)




    def calculateComplexityRate(qualityCodeResults, myQualityModel):
        try:
            aggregatedMetricsWeight = myQualityModel.violations_weight + myQualityModel.coverage_weight + myQualityModel.duplication_weight + myQualityModel.complexity_weight + myQualityModel.comments_weight 
            complexityScore = MIN_SCORE
            complexityWeightedScore = MIN_SCORE
            print ("  Evaluating Complexity Code rate...")
            print ("    Complexity in functions metric (SonarMetric): ", qualityCodeResults.complexity_in_functions)
            print ("    Number of functions (SonarMetric): ", qualityCodeResults.functions)
            averageComplexity =  qualityCodeResults.complexity_in_functions / qualityCodeResults.functions
            print ("    Average complexity per function: ", averageComplexity)
             
            
            # This is a NEGATIVE METRIC: HIHGER IS WORSE
            if averageComplexity > myQualityModel.complexity_levels[0]:
                score = MIN_SCORE
                print ("    Metric is higher than Score Level 1 (very bad!). Set Score to:", MIN_SCORE)
            elif averageComplexity < myQualityModel.complexity_levels[4]:
                score = MAX_SCORE
                print ("    Metric is lower than Score Level 5 (very good!). Set Score to:", MAX_SCORE)
            else:
                level = 1
                while ((level < 5) & (averageComplexity < myQualityModel.complexity_levels[level])):
                    level += 1
                # Reached Score is 1 point for each level reched plus a percentage of the current level (3-rule)
                partialScore = (myQualityModel.complexity_levels[level-1] - averageComplexity) / (myQualityModel.complexity_levels[level-1] - myQualityModel.complexity_levels[level])
                score = level - 1 + partialScore 
                print ("    Value is between Score Level ", level-1, " (", myQualityModel.complexity_levels[level-1], ") and ", level, " (", myQualityModel.complexity_levels[level], "). Set Score to:", score)
            
            weightedScore = (score * myQualityModel.complexity_weight) / aggregatedMetricsWeight
            
            # If Score is higher than MAX, apply a BONUS
            if averageComplexity < myQualityModel.complexity_min_value:
                weightedScore += myQualityModel.complexity_bonus;
                print ("    Score is higher than MAX --> BONUS [+", myQualityModel.complexity_bonus, "] applied.") 
            # If Score is lower than MIN, apply a PENALTY
            if averageComplexity > myQualityModel.complexity_max_value:
                weightedScore -= myQualityModel.complexity_penalty;
                print ("    Score is too low --> PENALTY [-", myQualityModel.complexity_penalty, "] applied.") 

            print ("    Complexity Code Metric Weight is ", myQualityModel.complexity_weight , " and Score is ",  score)
            print ("  Final Complexity Rated score (Weighted) is: ", weightedScore)
            print ("  ")            
            return weightedScore
        except Exception as e:
            print ("Error in QualityRateEvaluator.calculateComplexityRate: ", e)
            raise ValueError 
        except: # catch *all* exceptions
            print ("QualityRateEvaluator.calculateComplexityRate: ", e)
            e = sys.exc_info()[0]
            print ("EXCEPTION:", e)


            