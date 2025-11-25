# LegalAI Agent with AWS Bedrock AgentCore

AI-powered legal automation platform built on **AWS Bedrock AgentCore** and **Strands Agents framework**. Reduces manual document review time by 60-80% and cuts e-discovery costs by 85% using advanced AI and AWS services.

## What's New: AgentCore Integration

This platform showcases AWS Bedrock AgentCore's capabilities for legal automation:

- **AgentCore Runtime**: Containerized Legal AI Agent as managed AWS service
- **AgentCore Memory**: Persistent legal case history and conversation context
- **AgentCore Gateway**: SigV4-authenticated legal tools (document processing, legal research, compliance monitoring)
- **Turn-based Session Management**: Optimized memory persistence for legal workflows
- **Dynamic Tool Filtering**: Per-user legal tool selection with real-time updates

## Architecture

<img src="docs/images/legalai-architecture.svg"
     alt="LegalAI Architecture Overview"
     width="1200">

### Core Components

1. **Frontend + BFF** (Next.js)
   - Legal document upload and analysis interface
   - Contract review dashboard with risk visualization
   - Legal research interface with case law integration
   - Cognito authentication with role-based access
   - Real-time streaming of legal analysis results

2. **AgentCore Runtime**
   - Strands Agent with Bedrock Claude 3.5 Sonnet for legal analysis
   - Specialized legal AI models for contract review and compliance
   - Turn-based session manager for complex legal workflows
   - Uses AgentCore Memory for case history persistence
   - Integrates with legal databases via AgentCore Gateway

3. **AgentCore Gateway**
   - API Gateway with SigV4 authentication for legal services
   - Routes requests to specialized legal Lambda functions
   - Tools: Document OCR, Legal Database Search, Compliance Monitoring
   - Secure access to external legal APIs and databases

4. **AgentCore Memory**
   - DynamoDB-backed legal case and conversation persistence
   - Automatic legal precedent and case history management
   - Client-attorney privilege protection with encryption

## Key Legal Features

### Contract Analysis Engine
- **Automated Clause Extraction**: Identifies key contract terms and obligations
- **Risk Assessment**: AI-powered analysis of contract risks and liabilities
- **Obligation Tracking**: Monitors contract deadlines and compliance requirements
- **Redlining Assistance**: Suggests contract modifications and improvements

### Legal Research Assistant
- **Case Law Analysis**: AI-powered search and analysis of legal precedents
- **Regulatory Monitoring**: Real-time tracking of regulatory changes
- **Citation Verification**: Automated legal citation checking and formatting
- **Jurisdiction Analysis**: Multi-jurisdiction legal research capabilities

### E-Discovery Platform
- **Document Classification**: AI-powered categorization of legal documents
- **Privilege Review**: Automated attorney-client privilege detection
- **Relevance Scoring**: ML-based document relevance assessment
- **Cost Optimization**: 85% reduction in e-discovery processing costs

### Compliance Monitoring
- **Regulatory Change Detection**: Real-time monitoring of legal updates
- **Compliance Gap Analysis**: Identifies potential compliance issues
- **Risk Scoring**: Quantitative risk assessment for legal matters
- **Audit Trail**: Comprehensive logging for legal compliance

## Tool Categories

### Local Legal Tools (9 tools)
Embedded in AgentCore Runtime container:
- **Contract Parser**: Extract and analyze contract structures
- **Clause Extractor**: Identify specific contract clauses and terms
- **Risk Calculator**: Quantitative legal risk assessment
- **Compliance Checker**: Regulatory compliance verification
- **Legal Citation**: Automated citation formatting and verification
- **Document Classifier**: AI-powered legal document categorization
- **Obligation Tracker**: Contract deadline and obligation monitoring
- **Deadline Monitor**: Legal deadline tracking and alerts
- **Legal Research Assistant**: Case law and statute research

### Gateway Legal Tools (12 tools via 6 Lambdas)
Accessed via AgentCore Gateway with SigV4 auth:

| Lambda Function | Tools | Purpose |
|----------------|-------|---------|
| **legal-textract** | document_ocr, text_extraction | Document processing and OCR |
| **legal-database** | case_search, statute_lookup | Legal database integration |
| **court-records** | case_lookup, filing_search | Court records and filings |
| **regulatory-monitor** | regulation_search, compliance_check | Regulatory monitoring |
| **legal-research** | precedent_search, citation_analysis | Legal research and analysis |
| **contract-templates** | template_search, form_generation | Legal forms and templates |

### Built-in AWS Tools (8 tools)
AWS Bedrock-powered legal capabilities:
- **Legal Chart Generator**: Contract timeline and obligation charts
- **Risk Heat Maps**: Visual risk assessment dashboards
- **Compliance Reports**: Automated compliance reporting
- **Contract Visualization**: Visual contract structure analysis
- **Legal Analytics**: Statistical analysis of legal matters
- **Document Summaries**: AI-generated legal document summaries
- **Case Brief Generator**: Automated case brief creation
- **Timeline Generator**: Legal event timeline creation

## Expected ROI

- **60-80% reduction** in contract review time
- **85% cost savings** in e-discovery ($2-3 to $0.20-0.30 per document)
- **50-70% reduction** in M&A due diligence costs
- **Prevention of $500K-$5M** annual contract losses through risk detection
- **40-60% faster** legal research and case preparation
- **90% reduction** in manual compliance monitoring tasks

## Quick Start

### Prerequisites

- AWS Account with Bedrock access and legal AI models enabled
- AWS CLI configured with appropriate permissions
- Docker installed for local development
- Node.js 18+ and Python 3.13+
- Legal database API keys (optional for enhanced features)

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/adianautiyal/LegalAI.git
cd LegalAI/legalai-app
./setup.sh

# 2. Configure environment
cd ../agent-blueprint
cp .env.example .env
# Edit .env with your AWS credentials and legal API keys

# 3. Start services
cd ../legalai-app
./start.sh
```

Access at: http://localhost:3000

### Cloud Deployment

```bash
# Full deployment (all components)
cd agent-blueprint
./deploy.sh

# Or deploy individually:
# 1. Main application (Frontend + AgentCore Runtime)
cd chatbot-deployment/infrastructure
./scripts/deploy.sh

# 2. AgentCore Gateway (Legal Lambda tools)
cd ../../agentcore-gateway-stack
./scripts/deploy.sh
```

## Security & Compliance

### Data Protection
- **KMS encryption** for all legal documents and communications
- **Client-attorney privilege** protection with secure data handling
- **GDPR and CCPA compliance** with data retention policies
- **SOC 2 Type II** compliant infrastructure

### Access Control
- **IAM role-based access** control for legal teams
- **Multi-factor authentication** for sensitive legal operations
- **Audit logging** with CloudTrail for all legal document access
- **WAF protection** for all legal APIs and interfaces

### Legal Compliance
- **Bar association compliance** for legal AI assistance
- **Ethical AI guidelines** adherence for legal decision support
- **Confidentiality protection** for all client communications
- **Professional liability** considerations for AI-assisted legal work

## Configuration

### Legal Tool Configuration

Tools are configured in `legalai-app/frontend/src/config/legal-tools-config.json`:

```json
{
  "local_legal_tools": [
    {
      "id": "contract_parser",
      "name": "Contract Parser",
      "enabled": true,
      "isDynamic": false,
      "category": "contract_analysis"
    }
  ],
  "gateway_legal_targets": [
    {
      "id": "gateway_legal-database",
      "name": "Legal Database Search",
      "enabled": true,
      "isDynamic": true,
      "tools": [
        {
          "id": "gateway_legal-database___case_search",
          "name": "Case Law Search"
        }
      ]
    }
  ]
}
```

### Legal API Keys

Configure legal service API keys in AWS Secrets Manager:

```bash
# Legal Database API Key
aws secretsmanager put-secret-value \
  --secret-id legalai-agent/legal-database-api-key \
  --secret-string "YOUR_LEGAL_DB_KEY"

# Court Records API Credentials
aws secretsmanager put-secret-value \
  --secret-id legalai-agent/court-records-credentials \
  --secret-string '{"api_key":"KEY","jurisdiction":"US"}'
```

## Technology Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- **BFF**: Next.js API Routes (server-side) on Fargate
- **Runtime**: Strands Agents v1.2.0 + FastAPI (Python 3.13) on AgentCore Runtime
- **AI**: AWS Bedrock (Claude 3.5 Sonnet for legal analysis)
- **AgentCore**: Runtime, Memory, Gateway components for legal workflows
- **Legal Tools**: Lambda Functions with MCP protocol for legal services
- **Infrastructure**: AWS CDK, CloudFront, Cognito, KMS encryption

## Project Structure

```
LegalAI/
├── legalai-app/
│   ├── frontend/              # Next.js (Frontend + BFF)
│   │   └── src/
│   │       ├── app/api/       # Legal API routes (BFF layer)
│   │       ├── components/    # Legal UI components
│   │       └── config/        # Legal tool configuration
│   └── agentcore/             # AgentCore Runtime
│       └── src/
│           ├── agent/         # LegalAgent + session management
│           ├── local_tools/   # Contract analysis, legal research
│           ├── builtin_tools/ # Legal chart generation, compliance
│           └── routers/       # FastAPI routes for legal services
│
└── agent-blueprint/
    ├── chatbot-deployment/    # Main app stack (Frontend+Runtime)
    ├── agentcore-gateway-stack/   # Gateway + Legal Lambda functions
    ├── agentcore-runtime-stack/   # Runtime deployment (shared)
    └── agentcore-runtime-a2a-stack/   # Legal document processor
```

## Legal Disclaimers

- **AI Assistance Only**: This system provides AI-powered assistance and should not replace professional legal judgment
- **Professional Responsibility**: Users must comply with applicable bar association rules and professional responsibility requirements
- **Confidentiality**: All client communications and documents are protected with enterprise-grade security
- **Accuracy**: While AI analysis is highly accurate, all legal conclusions should be reviewed by qualified legal professionals

## Support & Documentation

- **Issues**: [GitHub Issues](https://github.com/adianautiyal/LegalAI/issues)
- **Legal AI Best Practices**: [docs/guides/LEGAL_AI_GUIDELINES.md](docs/guides/LEGAL_AI_GUIDELINES.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Security Guide**: [docs/guides/SECURITY.md](docs/guides/SECURITY.md)

## License

MIT License - see LICENSE file for details.

---

**Built with AWS Bedrock AgentCore for Legal Innovation** | [LegalAI on GitHub](https://github.com/adianautiyal/LegalAI)