"""
LegalAI Agent - Core legal AI agent with AgentCore integration
"""

from typing import List, Dict, Any, Optional
import logging
from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.memory.config import AgentCoreMemoryConfig

from ..local_tools.contract_analyzer import ContractAnalyzer
from ..local_tools.legal_research import LegalResearchTool
from ..local_tools.compliance_checker import ComplianceChecker
from ..local_tools.risk_calculator import RiskCalculator
from ..local_tools.document_classifier import DocumentClassifier
from ..local_tools.obligation_tracker import ObligationTracker
from ..local_tools.legal_citation import LegalCitationTool
from ..local_tools.deadline_monitor import DeadlineMonitor
from ..local_tools.clause_extractor import ClauseExtractor

logger = logging.getLogger(__name__)

class LegalAgent:
    """
    LegalAI Agent with specialized legal tools and AgentCore Memory integration
    """
    
    def __init__(self, session_id: str, user_id: str, memory_arn: str):
        """
        Initialize the Legal Agent with AgentCore Memory
        
        Args:
            session_id: Unique session identifier
            user_id: User identifier (typically from Cognito)
            memory_arn: ARN of the AgentCore Memory instance
        """
        self.session_id = session_id
        self.user_id = user_id
        
        # Configure AgentCore Memory for legal case persistence
        memory_config = AgentCoreMemoryConfig(
            memory_arn=memory_arn,
            max_tokens=15000  # Increased for complex legal documents
        )
        
        # Initialize session manager with legal-specific configuration
        self.session_manager = AgentCoreMemorySessionManager(
            session_id=session_id,
            memory_config=memory_config
        )
        
        # Initialize local legal tools
        self.local_tools = self._initialize_local_tools()
        
        # Initialize the Strands Agent with legal-optimized configuration
        self.agent = Agent(
            model=BedrockModel(
                model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
                temperature=0.1,  # Lower temperature for legal accuracy
                max_tokens=4000
            ),
            tools=self.local_tools,
            session_manager=self.session_manager,
            system_prompt=self._get_legal_system_prompt()
        )
        
        logger.info(f"LegalAgent initialized for session {session_id}, user {user_id}")
    
    def _initialize_local_tools(self) -> List[Any]:
        """Initialize all local legal tools"""
        return [
            ContractAnalyzer(),
            LegalResearchTool(),
            ComplianceChecker(),
            RiskCalculator(),
            DocumentClassifier(),
            ObligationTracker(),
            LegalCitationTool(),
            DeadlineMonitor(),
            ClauseExtractor()
        ]
    
    def _get_legal_system_prompt(self) -> str:
        """Get the legal-specific system prompt"""
        return """You are LegalAI, an advanced AI legal assistant designed to help legal professionals with:

1. CONTRACT ANALYSIS: Review contracts, identify key clauses, assess risks, and track obligations
2. LEGAL RESEARCH: Search case law, statutes, and regulations across multiple jurisdictions
3. COMPLIANCE MONITORING: Check regulatory compliance and identify potential issues
4. E-DISCOVERY: Classify documents, assess privilege, and manage document review
5. RISK ASSESSMENT: Quantify legal risks and provide mitigation strategies

IMPORTANT GUIDELINES:
- Always maintain attorney-client privilege and confidentiality
- Provide analysis and recommendations, but emphasize that final legal decisions require human judgment
- Cite relevant legal authorities when making recommendations
- Flag potential conflicts of interest or ethical considerations
- Use clear, professional legal language appropriate for legal professionals
- When analyzing contracts, focus on: terms, obligations, risks, deadlines, and compliance requirements
- For legal research, provide comprehensive analysis with proper citations
- Always recommend professional legal review for critical decisions

CAPABILITIES:
- Contract parsing and clause extraction
- Legal risk calculation and assessment
- Regulatory compliance checking
- Document classification and privilege review
- Legal citation formatting and verification
- Obligation and deadline tracking
- Case law and statute research
- Legal document drafting assistance

Remember: You are an AI assistant to legal professionals, not a replacement for legal judgment."""

    async def process_legal_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a legal query with context
        
        Args:
            query: The legal question or request
            context: Additional context (document metadata, case info, etc.)
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            # Add context to the query if provided
            if context:
                enhanced_query = f"Context: {context}\n\nQuery: {query}"
            else:
                enhanced_query = query
            
            # Process through the agent
            response = await self.agent.run(enhanced_query)
            
            return {
                "response": response,
                "session_id": self.session_id,
                "user_id": self.user_id,
                "context": context,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Error processing legal query: {str(e)}")
            return {
                "error": str(e),
                "session_id": self.session_id,
                "user_id": self.user_id
            }
    
    async def analyze_contract(self, document_content: str, contract_type: str = "general") -> Dict[str, Any]:
        """
        Specialized contract analysis
        
        Args:
            document_content: The contract text
            contract_type: Type of contract (employment, NDA, service, etc.)
            
        Returns:
            Comprehensive contract analysis
        """
        analysis_query = f"""
        Please perform a comprehensive analysis of this {contract_type} contract:

        {document_content}

        Provide analysis including:
        1. Key terms and clauses
        2. Obligations for each party
        3. Risk assessment
        4. Important deadlines
        5. Compliance considerations
        6. Recommended modifications or concerns
        """
        
        return await self.process_legal_query(analysis_query, {
            "document_type": "contract",
            "contract_type": contract_type,
            "analysis_type": "comprehensive"
        })
    
    async def research_legal_issue(self, legal_question: str, jurisdiction: str = "federal") -> Dict[str, Any]:
        """
        Conduct legal research on a specific issue
        
        Args:
            legal_question: The legal question to research
            jurisdiction: Relevant jurisdiction
            
        Returns:
            Legal research results with citations
        """
        research_query = f"""
        Please research the following legal issue for {jurisdiction} jurisdiction:

        {legal_question}

        Provide:
        1. Relevant case law and precedents
        2. Applicable statutes and regulations
        3. Legal analysis and interpretation
        4. Practical implications
        5. Proper legal citations
        """
        
        return await self.process_legal_query(research_query, {
            "research_type": "legal_issue",
            "jurisdiction": jurisdiction,
            "query_type": "research"
        })
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for logging"""
        from datetime import datetime
        return datetime.utcnow().isoformat()