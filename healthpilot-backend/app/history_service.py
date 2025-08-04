from typing import List, Dict, Any, Optional
from .database import DatabaseService
import logging

logger = logging.getLogger(__name__)

class HistoryService:
    def __init__(self):
        self.db_service = DatabaseService()
    
    def get_user_report_history(self, profile_id: str) -> List[Dict[str, Any]]:
        """Get all reports for a user"""
        try:
            # Use Supabase's query builder instead of raw SQL
            response = self.db_service.supabase.table("reports").select(
                "id, original_filename, report_date, lab_name, status, created_at"
            ).eq("profile_id", profile_id).order("created_at", desc=True).execute()
            
            reports = response.data if response.data else []
            
            # For each report, get the analysis data
            for report in reports:
                analysis_response = self.db_service.supabase.table("analyses").select(
                    "summary, risk_level, abnormal_count, critical_count"
                ).eq("report_id", report["id"]).execute()
                
                if analysis_response.data:
                    analysis = analysis_response.data[0]
                    report.update({
                        "summary": analysis.get("summary"),
                        "risk_level": analysis.get("risk_level"),
                        "abnormal_count": analysis.get("abnormal_count", 0),
                        "critical_count": analysis.get("critical_count", 0)
                    })
                else:
                    report.update({
                        "summary": None,
                        "risk_level": None,
                        "abnormal_count": 0,
                        "critical_count": 0
                    })
            
            return reports
            
        except Exception as e:
            logger.error(f"Error getting user history: {e}")
            return []
    
    def get_report_details(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific report"""
        try:
            # Get report details
            report_response = self.db_service.supabase.table("reports").select("*").eq("id", report_id).execute()
            
            if not report_response.data:
                return None
                
            report = report_response.data[0]
            
            # Get analysis details
            analysis_response = self.db_service.supabase.table("analyses").select("*").eq("report_id", report_id).execute()
            
            if analysis_response.data:
                analysis = analysis_response.data[0]
                report.update({
                    "analysis_result": analysis.get("analysis_result"),
                    "summary": analysis.get("summary"),
                    "risk_level": analysis.get("risk_level"),
                    "abnormal_count": analysis.get("abnormal_count", 0),
                    "critical_count": analysis.get("critical_count", 0)
                })
            else:
                report.update({
                    "analysis_result": None,
                    "summary": None,
                    "risk_level": None,
                    "abnormal_count": 0,
                    "critical_count": 0
                })
            
            # Get profile details
            if report.get("profile_id"):
                profile_response = self.db_service.supabase.table("profiles").select("email, age, sex").eq("id", report["profile_id"]).execute()
                
                if profile_response.data:
                    profile = profile_response.data[0]
                    report.update({
                        "email": profile.get("email"),
                        "age": profile.get("age"),
                        "sex": profile.get("sex")
                    })
            
            return report
            
        except Exception as e:
            logger.error(f"Error getting report details: {e}")
            return None
    
    def get_test_trends(self, profile_id: str, test_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trend data for a specific test"""
        try:
            response = self.db_service.supabase.table("test_trends").select(
                "test_value, test_unit, classification, reference_range, report_date, created_at"
            ).eq("profile_id", profile_id).eq("test_name", test_name).order("report_date", desc=True).limit(limit).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            logger.error(f"Error getting test trends: {e}")
            return []
    
    def compare_reports(self, report_id_1: str, report_id_2: str) -> Dict[str, Any]:
        """Compare two reports"""
        try:
            # Get both reports
            report_1 = self.get_report_details(report_id_1)
            report_2 = self.get_report_details(report_id_2)
            
            if not report_1 or not report_2:
                return {"error": "One or both reports not found"}
            
            # Extract test results for comparison
            analysis_1 = report_1.get('analysis_result', {})
            analysis_2 = report_2.get('analysis_result', {})
            
            results_1 = analysis_1.get('results', [])
            results_2 = analysis_2.get('results', [])
            
            # Create comparison data
            comparison = {
                "report_1": {
                    "id": report_id_1,
                    "date": report_1.get('report_date'),
                    "summary": report_1.get('summary'),
                    "risk_level": report_1.get('risk_level'),
                    "results": results_1
                },
                "report_2": {
                    "id": report_id_2,
                    "date": report_2.get('report_date'),
                    "summary": report_2.get('summary'),
                    "risk_level": report_2.get('risk_level'),
                    "results": results_2
                },
                "changes": self._calculate_changes(results_1, results_2)
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing reports: {e}")
            return {"error": str(e)}
    
    def _calculate_changes(self, results_1: List[Dict], results_2: List[Dict]) -> List[Dict[str, Any]]:
        """Calculate changes between two sets of results"""
        changes = []
        
        # Create lookup dictionaries
        results_1_dict = {r['test_name']: r for r in results_1}
        results_2_dict = {r['test_name']: r for r in results_2}
        
        # Find all unique test names
        all_tests = set(results_1_dict.keys()) | set(results_2_dict.keys())
        
        for test_name in all_tests:
            result_1 = results_1_dict.get(test_name)
            result_2 = results_2_dict.get(test_name)
            
            if result_1 and result_2:
                # Both reports have this test
                value_1 = result_1.get('value', 0)
                value_2 = result_2.get('value', 0)
                change = value_2 - value_1
                change_percent = ((value_2 - value_1) / value_1 * 100) if value_1 != 0 else 0
                
                changes.append({
                    "test_name": test_name,
                    "value_1": value_1,
                    "value_2": value_2,
                    "change": change,
                    "change_percent": round(change_percent, 2),
                    "unit": result_1.get('unit', ''),
                    "classification_1": result_1.get('classification', ''),
                    "classification_2": result_2.get('classification', ''),
                    "status": "improved" if change < 0 else "worsened" if change > 0 else "unchanged"
                })
            elif result_1:
                # Only in first report
                changes.append({
                    "test_name": test_name,
                    "value_1": result_1.get('value', 0),
                    "value_2": None,
                    "change": None,
                    "change_percent": None,
                    "unit": result_1.get('unit', ''),
                    "classification_1": result_1.get('classification', ''),
                    "classification_2": None,
                    "status": "removed"
                })
            elif result_2:
                # Only in second report
                changes.append({
                    "test_name": test_name,
                    "value_1": None,
                    "value_2": result_2.get('value', 0),
                    "change": None,
                    "change_percent": None,
                    "unit": result_2.get('unit', ''),
                    "classification_1": None,
                    "classification_2": result_2.get('classification', ''),
                    "status": "added"
                })
        
        return changes