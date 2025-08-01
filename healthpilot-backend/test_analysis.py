from app.analysis_engine import AnalysisEngine

# Test the analysis engine
engine = AnalysisEngine()

test_text = """
Glucose: 120 mg/dL
Hemoglobin: 14.2 g/dL
HDL: 45 mg/dL
LDL: 110 mg/dL
"""

result = engine.analyze_lab_report(test_text, age=30, sex="male")
print("Analysis result:")
print(result)
