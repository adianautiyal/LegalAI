"""
Contract Analyzer Tool - Specialized contract analysis and clause extraction
"""

from typing import Dict, List, Any, Optional
import re
import json
from datetime import datetime, timedelta
from strands.tools import Tool

class ContractAnalyzer(Tool):
    """
    Advanced contract analysis tool for legal document processing
    """
    
    name = "contract_analyzer"
    description = "Analyze contracts to extract key clauses, terms, obligations, and risks"
    
    def __init__(self):
        super().__init__()
        self.clause_patterns = self._initialize_clause_patterns()
        self.risk_indicators = self._initialize_risk_indicators()
    
    def _initialize_clause_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for common contract clauses"""
        return {
            "termination": [
                r"terminat[ei].*clause",
                r"end.*agreement",
                r"breach.*contract",
                r"notice.*terminat"
            ],
            "payment": [
                r"payment.*terms",
                r"invoice.*\d+.*days",
                r"net.*\d+",
                r"payment.*due"
            ],
            "liability": [
                r"limitation.*liability",
                r"indemnif.*",
                r"damages.*limited",
                r"liability.*cap"
            ],
            "intellectual_property": [
                r"intellectual.*property",
                r"copyright.*",
                r"trademark.*",
                r"proprietary.*information"
            ],
            "confidentiality": [
                r"confidential.*information",
                r"non.*disclosure",
                r"proprietary.*data",
                r"trade.*secret"
            ],
            "governing_law": [
                r"governing.*law",
                r"jurisdiction.*",
                r"applicable.*law",
                r"courts.*of.*"
            ]
        }
    
    def _initialize_risk_indicators(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate potential risks"""
        return {
            "high_risk": [
                r"unlimited.*liability",
                r"personal.*guarantee",
                r"liquidated.*damages",
                r"automatic.*renewal"
            ],
            "medium_risk": [
                r"penalty.*clause",
                r"exclusive.*dealing",
                r"non.*compete",
                r"minimum.*purchase"
            ],
            "compliance_risk": [
                r"regulatory.*compliance",
                r"data.*protection",
                r"privacy.*policy",
                r"gdpr.*compliance"
            ]
        }
    
    async def run(self, contract_text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze contract and extract key information
        
        Args:
            contract_text: The contract content to analyze
            analysis_type: Type of analysis (comprehensive, quick, specific)
            
        Returns:
            Detailed contract analysis
        """
        try:
            analysis = {
                "contract_summary": self._generate_summary(contract_text),
                "key_clauses": self._extract_clauses(contract_text),
                "obligations": self._extract_obligations(contract_text),
                "risk_assessment": self._assess_risks(contract_text),
                "important_dates": self._extract_dates(contract_text),
                "parties": self._identify_parties(contract_text),
                "financial_terms": self._extract_financial_terms(contract_text),
                "compliance_requirements": self._check_compliance(contract_text),
                "recommendations": self._generate_recommendations(contract_text)
            }
            
            if analysis_type == "comprehensive":
                analysis["detailed_analysis"] = self._detailed_analysis(contract_text)
            
            return {
                "success": True,
                "analysis": analysis,
                "analysis_type": analysis_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate a high-level contract summary"""
        word_count = len(text.split())
        
        # Identify contract type
        contract_type = "General Agreement"
        if re.search(r"employment.*agreement", text, re.IGNORECASE):
            contract_type = "Employment Agreement"
        elif re.search(r"service.*agreement", text, re.IGNORECASE):
            contract_type = "Service Agreement"
        elif re.search(r"non.*disclosure", text, re.IGNORECASE):
            contract_type = "Non-Disclosure Agreement"
        elif re.search(r"purchase.*agreement", text, re.IGNORECASE):
            contract_type = "Purchase Agreement"
        
        return {
            "contract_type": contract_type,
            "word_count": word_count,
            "estimated_complexity": "High" if word_count > 5000 else "Medium" if word_count > 2000 else "Low",
            "key_sections_identified": len(self._extract_clauses(text))
        }
    
    def _extract_clauses(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract and categorize contract clauses"""
        clauses = {}
        
        for clause_type, patterns in self.clause_patterns.items():
            clauses[clause_type] = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Extract surrounding context
                    start = max(0, match.start() - 200)
                    end = min(len(text), match.end() + 200)
                    context = text[start:end].strip()
                    
                    clauses[clause_type].append({
                        "matched_text": match.group(),
                        "context": context,
                        "position": match.start(),
                        "confidence": 0.8  # Basic confidence score
                    })
        
        return clauses
    
    def _extract_obligations(self, text: str) -> List[Dict[str, Any]]:
        """Extract obligations for each party"""
        obligations = []
        
        # Patterns for obligation identification
        obligation_patterns = [
            r"shall.*",
            r"must.*",
            r"required.*to.*",
            r"obligated.*to.*",
            r"responsible.*for.*"
        ]
        
        for pattern in obligation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract sentence containing the obligation
                sentence_start = text.rfind('.', 0, match.start()) + 1
                sentence_end = text.find('.', match.end())
                if sentence_end == -1:
                    sentence_end = len(text)
                
                obligation_text = text[sentence_start:sentence_end].strip()
                
                obligations.append({
                    "obligation": obligation_text,
                    "type": "contractual_duty",
                    "position": match.start(),
                    "urgency": self._assess_obligation_urgency(obligation_text)
                })
        
        return obligations[:10]  # Limit to top 10 obligations
    
    def _assess_risks(self, text: str) -> Dict[str, Any]:
        """Assess contract risks"""
        risks = {
            "high_risk_items": [],
            "medium_risk_items": [],
            "compliance_risks": [],
            "overall_risk_score": 0
        }
        
        total_risk_score = 0
        
        for risk_level, patterns in self.risk_indicators.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                
                for match in matches:
                    risk_item = {
                        "risk_text": match.group(),
                        "risk_level": risk_level,
                        "position": match.start(),
                        "mitigation_needed": True
                    }
                    
                    if risk_level == "high_risk":
                        risks["high_risk_items"].append(risk_item)
                        total_risk_score += 3
                    elif risk_level == "medium_risk":
                        risks["medium_risk_items"].append(risk_item)
                        total_risk_score += 2
                    elif risk_level == "compliance_risk":
                        risks["compliance_risks"].append(risk_item)
                        total_risk_score += 2
        
        # Calculate overall risk score (0-10 scale)
        risks["overall_risk_score"] = min(10, total_risk_score)
        
        return risks
    
    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract important dates and deadlines"""
        date_patterns = [
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
            r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}",
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}"
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract context around the date
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                dates.append({
                    "date": match.group(),
                    "context": context,
                    "position": match.start(),
                    "type": self._classify_date_type(context)
                })
        
        return dates[:5]  # Limit to top 5 dates
    
    def _identify_parties(self, text: str) -> List[Dict[str, Any]]:
        """Identify contract parties"""
        # Simple party identification - can be enhanced
        party_patterns = [
            r"\"([^\"]+)\"\s*\(.*party.*\)",
            r"between\s+([^,]+),",
            r"party.*\"([^\"]+)\""
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                party_name = match.group(1).strip()
                if len(party_name) > 3 and len(party_name) < 100:
                    parties.append({
                        "name": party_name,
                        "type": "contracting_party",
                        "position": match.start()
                    })
        
        return parties[:5]  # Limit to top 5 parties
    
    def _extract_financial_terms(self, text: str) -> Dict[str, Any]:
        """Extract financial terms and amounts"""
        financial_patterns = [
            r"\$[\d,]+\.?\d*",
            r"payment.*\$[\d,]+",
            r"fee.*\$[\d,]+",
            r"cost.*\$[\d,]+"
        ]
        
        financial_terms = []
        for pattern in financial_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                financial_terms.append({
                    "amount": match.group(),
                    "position": match.start(),
                    "type": "monetary_amount"
                })
        
        return {
            "financial_terms": financial_terms[:10],
            "total_amounts_found": len(financial_terms)
        }
    
    def _check_compliance(self, text: str) -> List[Dict[str, Any]]:
        """Check for compliance requirements"""
        compliance_patterns = [
            r"gdpr.*compliance",
            r"data.*protection",
            r"privacy.*policy",
            r"regulatory.*requirement",
            r"compliance.*with.*law"
        ]
        
        compliance_items = []
        for pattern in compliance_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                compliance_items.append({
                    "requirement": match.group(),
                    "type": "compliance_obligation",
                    "position": match.start(),
                    "priority": "high"
                })
        
        return compliance_items
    
    def _generate_recommendations(self, text: str) -> List[str]:
        """Generate contract recommendations"""
        recommendations = []
        
        # Check for missing clauses
        if not re.search(r"limitation.*liability", text, re.IGNORECASE):
            recommendations.append("Consider adding a liability limitation clause")
        
        if not re.search(r"governing.*law", text, re.IGNORECASE):
            recommendations.append("Specify governing law and jurisdiction")
        
        if not re.search(r"terminat.*clause", text, re.IGNORECASE):
            recommendations.append("Include clear termination provisions")
        
        # Check for risk factors
        if re.search(r"unlimited.*liability", text, re.IGNORECASE):
            recommendations.append("Review unlimited liability provisions - consider limitations")
        
        if len(recommendations) == 0:
            recommendations.append("Contract appears to have standard provisions")
        
        return recommendations
    
    def _detailed_analysis(self, text: str) -> Dict[str, Any]:
        """Perform detailed contract analysis"""
        return {
            "clause_coverage": self._analyze_clause_coverage(text),
            "legal_language_complexity": self._analyze_language_complexity(text),
            "enforceability_assessment": self._assess_enforceability(text)
        }
    
    def _analyze_clause_coverage(self, text: str) -> Dict[str, bool]:
        """Analyze which standard clauses are present"""
        standard_clauses = [
            "termination", "payment", "liability", "intellectual_property",
            "confidentiality", "governing_law", "dispute_resolution"
        ]
        
        coverage = {}
        for clause in standard_clauses:
            patterns = self.clause_patterns.get(clause, [])
            coverage[clause] = any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)
        
        return coverage
    
    def _analyze_language_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze the complexity of legal language"""
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        return {
            "average_sentence_length": round(avg_sentence_length, 2),
            "complexity_level": "High" if avg_sentence_length > 25 else "Medium" if avg_sentence_length > 15 else "Low",
            "total_sentences": len(sentences)
        }
    
    def _assess_enforceability(self, text: str) -> Dict[str, Any]:
        """Basic enforceability assessment"""
        enforceability_factors = {
            "has_consideration": bool(re.search(r"consideration|payment|exchange", text, re.IGNORECASE)),
            "has_signatures": bool(re.search(r"signature|signed|execute", text, re.IGNORECASE)),
            "has_dates": bool(re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text)),
            "has_parties": bool(re.search(r"party|parties|between", text, re.IGNORECASE))
        }
        
        enforceability_score = sum(enforceability_factors.values()) / len(enforceability_factors)
        
        return {
            "enforceability_factors": enforceability_factors,
            "enforceability_score": round(enforceability_score, 2),
            "assessment": "Strong" if enforceability_score > 0.8 else "Moderate" if enforceability_score > 0.5 else "Weak"
        }
    
    def _assess_obligation_urgency(self, obligation_text: str) -> str:
        """Assess the urgency of an obligation"""
        urgent_keywords = ["immediately", "within", "days", "deadline", "before"]
        
        if any(keyword in obligation_text.lower() for keyword in urgent_keywords):
            return "high"
        return "medium"
    
    def _classify_date_type(self, context: str) -> str:
        """Classify the type of date based on context"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ["effective", "commence", "start"]):
            return "effective_date"
        elif any(word in context_lower for word in ["expire", "end", "terminate"]):
            return "expiration_date"
        elif any(word in context_lower for word in ["payment", "due", "invoice"]):
            return "payment_date"
        else:
            return "general_date"