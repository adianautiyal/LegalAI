# LegalAI Agent Project Structure

This document explains the complete project structure and organization of the LegalAI Agent with AWS Bedrock AgentCore.

## Overview

The LegalAI project follows the AWS Bedrock AgentCore pattern with specialized legal tools and services. The architecture is designed for enterprise legal automation with security, compliance, and scalability in mind.

```
LegalAI/
├── docs/                           # Documentation and diagrams
├── legalai-app/                    # Main application code
├── agent-blueprint/                # Infrastructure and deployment
├── tests/                          # Test suites
└── Configuration files
```

## Detailed Structure

### Root Directory

```
LegalAI/
├── README.md                       # Main project documentation
├── DEPLOYMENT.md                   # Deployment guide
├── PROJECT_STRUCTURE.md           # This file
├── LICENSE                         # MIT License
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment template
└── requirements.txt                # Python dependencies
```

### Documentation (`docs/`)

```
docs/
├── images/
│   └── legalai-architecture.svg    # Architecture diagram
├── guides/
│   ├── LEGAL_AI_GUIDELINES.md     # Legal AI best practices
│   ├── SECURITY.md                # Security guidelines
│   ├── COMPLIANCE.md              # Legal compliance guide
│   └── TROUBLESHOOTING.md         # Common issues and solutions
├── api/
│   ├── API_REFERENCE.md           # Complete API documentation
│   └── LEGAL_TOOLS.md             # Legal tools documentation
└── examples/
    ├── contract-analysis.md        # Contract analysis examples
    ├── legal-research.md           # Legal research examples
    └── compliance-monitoring.md    # Compliance examples
```

### Main Application (`legalai-app/`)

The core application following AgentCore patterns:

```
legalai-app/
├── frontend/                       # Next.js Frontend + BFF
│   ├── src/
│   │   ├── app/                   # Next.js 13+ app directory
│   │   │   ├── api/               # API routes (BFF layer)
│   │   │   │   ├── chat/          # Chat endpoints
│   │   │   │   ├── legal/         # Legal service endpoints
│   │   │   │   ├── auth/          # Authentication
│   │   │   │   └── health/        # Health checks
│   │   │   ├── dashboard/         # Legal dashboard pages
│   │   │   ├── contracts/         # Contract analysis UI
│   │   │   ├── research/          # Legal research UI
│   │   │   └── compliance/        # Compliance monitoring UI
│   │   ├── components/            # React components
│   │   │   ├── legal/             # Legal-specific components
│   │   │   │   ├── ContractAnalyzer.tsx
│   │   │   │   ├── LegalResearch.tsx
│   │   │   │   ├── ComplianceMonitor.tsx
│   │   │   │   └── RiskAssessment.tsx
│   │   │   ├── ui/                # Reusable UI components
│   │   │   └── chat/              # Chat interface components
│   │   ├── config/                # Configuration files
│   │   │   ├── legal-tools-config.json
│   │   │   ├── api.ts
│   │   │   └── environment.ts
│   │   ├── hooks/                 # React hooks
│   │   │   ├── useLegalChat.ts
│   │   │   ├── useContractAnalysis.ts
│   │   │   └── useLegalResearch.ts
│   │   ├── lib/                   # Utility libraries
│   │   │   ├── legal-utils.ts
│   │   │   ├── api-client.ts
│   │   │   └── auth-utils.ts
│   │   ├── types/                 # TypeScript definitions
│   │   │   ├── legal.ts
│   │   │   ├── chat.ts
│   │   │   └── api.ts
│   │   └── utils/                 # Helper functions
│   ├── public/                    # Static assets
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── agentcore/                     # AgentCore Runtime
    ├── src/
    │   ├── agent/                 # Core agent implementation
    │   │   ├── legal_agent.py     # Main LegalAI agent
    │   │   ├── session_manager.py # Session management
    │   │   └── gateway_client.py  # Gateway integration
    │   ├── local_tools/           # Local legal tools
    │   │   ├── contract_analyzer.py
    │   │   ├── legal_research.py
    │   │   ├── compliance_checker.py
    │   │   ├── risk_calculator.py
    │   │   ├── document_classifier.py
    │   │   ├── obligation_tracker.py
    │   │   ├── legal_citation.py
    │   │   ├── deadline_monitor.py
    │   │   └── clause_extractor.py
    │   ├── builtin_tools/         # AWS Bedrock tools
    │   │   ├── legal_chart_generator.py
    │   │   ├── compliance_reporter.py
    │   │   └── document_summarizer.py
    │   ├── routers/               # FastAPI routers
    │   │   ├── chat.py
    │   │   ├── health.py
    │   │   ├── tools.py
    │   │   └── legal_services.py
    │   ├── models/                # Data models
    │   │   ├── schemas.py
    │   │   └── legal_models.py
    │   ├── streaming/             # Event streaming
    │   │   ├── event_processor.py
    │   │   └── event_formatter.py
    │   └── main.py                # FastAPI application
    ├── requirements.txt
    └── Dockerfile
```

### Infrastructure (`agent-blueprint/`)

AWS CDK infrastructure and deployment scripts:

```
agent-blueprint/
├── agentcore-gateway-stack/       # AgentCore Gateway
│   ├── infrastructure/            # CDK infrastructure
│   │   ├── bin/
│   │   │   └── gateway-stack.ts
│   │   ├── lib/
│   │   │   ├── gateway-stack.ts
│   │   │   ├── lambda-stack.ts
│   │   │   └── iam-stack.ts
│   │   ├── package.json
│   │   ├── cdk.json
│   │   └── tsconfig.json
│   ├── lambda-functions/          # Legal Lambda functions
│   │   ├── legal-textract/        # Document OCR
│   │   │   ├── lambda_function.py
│   │   │   └── requirements.txt
│   │   ├── legal-database/        # Legal DB search
│   │   │   ├── lambda_function.py
│   │   │   └── requirements.txt
│   │   ├── court-records/         # Court records API
│   │   │   ├── lambda_function.py
│   │   │   └── requirements.txt
│   │   ├── regulatory-monitor/    # Regulatory monitoring
│   │   │   ├── lambda_function.py
│   │   │   └── requirements.txt
│   │   ├── legal-research/        # Legal research tools
│   │   │   ├── lambda_function.py
│   │   │   └── requirements.txt
│   │   └── contract-templates/    # Legal templates
│   │       ├── lambda_function.py
│   │       └── requirements.txt
│   └── scripts/
│       ├── build-lambdas.sh
│       ├── deploy.sh
│       └── destroy.sh
│
├── agentcore-runtime-stack/       # AgentCore Runtime
│   ├── bin/
│   │   └── agentcore-runtime-stack.ts
│   ├── lib/
│   │   └── agent-runtime-stack.ts
│   ├── package.json
│   ├── cdk.json
│   └── tsconfig.json
│
├── chatbot-deployment/            # Main application stack
│   ├── infrastructure/
│   │   ├── bin/
│   │   │   └── app.ts
│   │   ├── lib/
│   │   │   ├── frontend-stack.ts
│   │   │   ├── cognito-auth-stack.ts
│   │   │   └── monitoring-stack.ts
│   │   ├── scripts/
│   │   │   ├── deploy.sh
│   │   │   └── destroy.sh
│   │   ├── package.json
│   │   ├── cdk.json
│   │   └── config.json
│   └── README.md
│
├── agentcore-runtime-a2a-stack/   # Agent-to-Agent (future)
│   └── legal-document-processor/
│       ├── cdk/
│       ├── src/
│       └── deploy.sh
│
├── deploy.sh                      # Main deployment script
├── destroy.sh                     # Cleanup script
└── .env.example                   # Environment template
```

### Tests (`tests/`)

Comprehensive test suites for all components:

```
tests/
├── unit/                          # Unit tests
│   ├── agent/
│   │   ├── test_legal_agent.py
│   │   └── test_session_manager.py
│   ├── tools/
│   │   ├── test_contract_analyzer.py
│   │   ├── test_legal_research.py
│   │   └── test_compliance_checker.py
│   └── api/
│       ├── test_chat_endpoints.py
│       └── test_legal_endpoints.py
│
├── integration/                   # Integration tests
│   ├── test_agentcore_integration.py
│   ├── test_gateway_integration.py
│   └── test_end_to_end.py
│
├── performance/                   # Performance tests
│   ├── test_contract_analysis_performance.py
│   └── test_concurrent_sessions.py
│
├── security/                      # Security tests
│   ├── test_authentication.py
│   ├── test_data_protection.py
│   └── test_privilege_protection.py
│
├── legal/                         # Legal-specific tests
│   ├── test_contract_samples/
│   ├── test_legal_accuracy.py
│   └── test_compliance_validation.py
│
├── fixtures/                      # Test data
│   ├── sample_contracts/
│   ├── legal_documents/
│   └── test_cases/
│
├── conftest.py                    # Pytest configuration
├── requirements.txt               # Test dependencies
└── README.md                      # Testing guide
```

## Key Components Explained

### 1. LegalAI Agent (`legalai-app/agentcore/src/agent/legal_agent.py`)

The core AI agent with legal specialization:
- **AgentCore Memory Integration**: Persistent legal case history
- **Legal Tool Orchestration**: Manages 20+ legal tools
- **Session Management**: Turn-based conversations for complex legal workflows
- **Security**: Attorney-client privilege protection

### 2. Local Legal Tools (`legalai-app/agentcore/src/local_tools/`)

Embedded legal processing tools:
- **Contract Analyzer**: Clause extraction, risk assessment, obligation tracking
- **Legal Research**: Case law search, statute lookup, citation verification
- **Compliance Checker**: Regulatory compliance validation
- **Risk Calculator**: Quantitative legal risk assessment
- **Document Classifier**: AI-powered legal document categorization

### 3. AgentCore Gateway (`agent-blueprint/agentcore-gateway-stack/`)

Secure access to external legal services:
- **SigV4 Authentication**: Secure API access
- **MCP Protocol**: Standardized tool communication
- **Legal APIs**: Integration with legal databases and services
- **Scalable Lambda Functions**: Auto-scaling legal service processing

### 4. Frontend Application (`legalai-app/frontend/`)

Professional legal interface:
- **Contract Analysis Dashboard**: Visual contract review and analysis
- **Legal Research Interface**: Case law and statute research
- **Compliance Monitoring**: Real-time regulatory compliance tracking
- **Document Management**: Secure legal document handling
- **Role-based Access**: Different interfaces for lawyers, paralegals, compliance teams

## Data Flow

### 1. Document Upload and Analysis
```
User uploads contract → Frontend validates → S3 storage (encrypted) → 
Textract OCR → Contract Analyzer → Risk Assessment → Results Dashboard
```

### 2. Legal Research Query
```
User query → Legal Research Tool → Gateway APIs → Legal Databases → 
Case Law Analysis → Citation Verification → Formatted Results
```

### 3. Compliance Monitoring
```
Regulatory changes → Monitoring APIs → Compliance Checker → 
Risk Assessment → Alert Generation → Dashboard Notification
```

## Security Architecture

### Data Protection Layers
1. **Encryption at Rest**: KMS encryption for all legal documents
2. **Encryption in Transit**: TLS 1.3 for all communications
3. **Access Control**: IAM roles, Cognito authentication, MFA
4. **Audit Logging**: Complete audit trail with CloudTrail
5. **Data Isolation**: Client data segregation and privilege protection

### Compliance Features
- **Attorney-Client Privilege**: Secure data handling and isolation
- **Data Retention**: Configurable retention policies (7+ years)
- **Audit Trail**: Comprehensive logging for legal compliance
- **Access Controls**: Role-based access for legal teams
- **Data Residency**: Configurable data location requirements

## Deployment Architecture

### Development Environment
- Local development with Docker Compose
- Mock legal APIs for testing
- Sample legal documents for development

### Staging Environment
- Full AWS deployment with test data
- Integration testing with real APIs
- Performance and security testing

### Production Environment
- Multi-AZ deployment for high availability
- Auto-scaling based on demand
- Comprehensive monitoring and alerting
- Disaster recovery and backup

## Monitoring and Observability

### Application Metrics
- Contract analysis processing time
- Legal research query performance
- Document classification accuracy
- User session analytics

### Business Metrics
- Cost savings from automation
- Time reduction in legal processes
- Risk mitigation effectiveness
- Compliance monitoring coverage

### Security Metrics
- Authentication success/failure rates
- Data access patterns
- Privilege escalation attempts
- Audit log completeness

## Future Enhancements

### Planned Features
- **Multi-language Support**: International legal document processing
- **Advanced Analytics**: Legal trend analysis and predictions
- **Workflow Automation**: End-to-end legal process automation
- **Integration Hub**: Connections to popular legal software

### Scalability Improvements
- **Global Deployment**: Multi-region legal document processing
- **Edge Computing**: Faster document processing with edge locations
- **Advanced Caching**: Intelligent caching for legal research results
- **Microservices**: Further decomposition for better scalability

---

This project structure is designed to be modular, scalable, and maintainable while meeting the stringent requirements of legal technology applications.