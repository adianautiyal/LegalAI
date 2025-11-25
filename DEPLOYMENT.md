# LegalAI Agent Deployment Guide

This guide provides step-by-step instructions for deploying the LegalAI Agent with AWS Bedrock AgentCore.

## Prerequisites

### AWS Account Setup
- AWS Account with Bedrock access enabled
- AWS CLI configured with appropriate permissions
- Bedrock model access for Claude 3.5 Sonnet
- AgentCore service enabled in your region

### Local Development Environment
- Node.js 18+ and npm
- Python 3.13+
- Docker Desktop
- AWS CDK CLI (`npm install -g aws-cdk`)
- Git

### Required AWS Permissions
Your AWS user/role needs permissions for:
- Bedrock (model access and AgentCore)
- Lambda, API Gateway, CloudFormation
- S3, DynamoDB, Secrets Manager
- IAM role creation
- CloudFront, Cognito

## Quick Start Deployment

### 1. Clone and Configure

```bash
git clone https://github.com/adianautiyal/LegalAI.git
cd LegalAI
cp .env.example .env
```

Edit `.env` with your AWS account details:
```bash
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id
STACK_PREFIX=legalai
ENVIRONMENT=dev
```

### 2. Deploy All Components

```bash
cd agent-blueprint
./deploy.sh
```

This will deploy:
- AgentCore Runtime (containerized legal agent)
- AgentCore Gateway (legal API tools)
- Frontend application with authentication
- Required AWS infrastructure

### 3. Configure API Keys

After deployment, update secrets in AWS Secrets Manager:

```bash
# Legal Database API Key
aws secretsmanager put-secret-value \
  --secret-id legalai-legal-database-api-key \
  --secret-string "your-legal-db-api-key"

# Court Records API
aws secretsmanager put-secret-value \
  --secret-id legalai-court-records-credentials \
  --secret-string '{"api_key":"your-key","jurisdiction":"US"}'
```

## Component-by-Component Deployment

### AgentCore Runtime

The runtime hosts the legal AI agent with specialized tools:

```bash
cd agent-blueprint
./deploy.sh runtime
```

**What it deploys:**
- Containerized Strands Agent with legal tools
- AgentCore Memory for conversation persistence
- Legal document processing capabilities
- Contract analysis and risk assessment tools

### AgentCore Gateway

The gateway provides secure access to external legal services:

```bash
./deploy.sh gateway
```

**What it deploys:**
- API Gateway with SigV4 authentication
- Lambda functions for legal services:
  - Document OCR (Textract integration)
  - Legal database search
  - Court records lookup
  - Regulatory monitoring
  - Legal research tools

### Main Application

The frontend and backend-for-frontend:

```bash
./deploy.sh app
```

**What it deploys:**
- Next.js frontend with legal UI components
- Cognito authentication
- CloudFront distribution
- Application Load Balancer
- ECS Fargate service

## Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Core AWS Settings
AWS_REGION=us-east-1
STACK_PREFIX=legalai
ENVIRONMENT=dev

# AgentCore Settings
AGENTCORE_MEMORY_ARN=arn:aws:bedrock-agentcore:region:account:memory/mem-id
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# Legal API Configuration
LEGAL_DATABASE_SECRET_NAME=legalai-legal-database-api-key
COURT_RECORDS_SECRET_NAME=legalai-court-records-credentials

# Security Settings
ATTORNEY_CLIENT_PRIVILEGE_PROTECTION=true
DATA_RETENTION_DAYS=2555
AUDIT_LOGGING=true
```

### Legal Tool Configuration

Configure which legal tools are available in `legalai-app/frontend/src/config/legal-tools-config.json`:

```json
{
  "local_legal_tools": [
    {
      "id": "contract_analyzer",
      "name": "Contract Analyzer",
      "enabled": true,
      "category": "contract_analysis"
    },
    {
      "id": "legal_research",
      "name": "Legal Research",
      "enabled": true,
      "category": "research"
    }
  ],
  "gateway_legal_targets": [
    {
      "id": "legal_database",
      "name": "Legal Database Search",
      "enabled": true,
      "tools": ["case_search", "statute_lookup"]
    }
  ]
}
```

## Security Configuration

### Data Protection

The LegalAI agent implements enterprise-grade security:

1. **Encryption at Rest**: All documents encrypted with KMS
2. **Encryption in Transit**: TLS 1.3 for all communications
3. **Attorney-Client Privilege**: Secure data handling and isolation
4. **Access Control**: IAM roles and Cognito authentication
5. **Audit Logging**: Complete audit trail with CloudTrail

### Compliance Settings

Configure compliance features:

```bash
# Enable attorney-client privilege protection
ATTORNEY_CLIENT_PRIVILEGE_PROTECTION=true

# Set legal document retention (7 years default)
DATA_RETENTION_DAYS=2555

# Enable comprehensive audit logging
AUDIT_LOGGING=true

# Configure data residency
DATA_RESIDENCY_REGION=us-east-1
```

## Monitoring and Observability

### CloudWatch Integration

The deployment automatically sets up:
- Application logs in CloudWatch
- Performance metrics and dashboards
- Error tracking and alerting
- Legal document processing metrics

### Custom Metrics

Key metrics tracked:
- Contract analysis processing time
- Legal research query response time
- Document classification accuracy
- User session duration
- API error rates

### Alerts

Configure alerts for:
- High error rates in legal processing
- Unusual document access patterns
- Performance degradation
- Security events

## Troubleshooting

### Common Issues

**1. AgentCore Memory Not Found**
```bash
# Check if AgentCore is enabled in your region
aws bedrock-agentcore list-memories --region us-east-1

# Create memory if needed
aws bedrock-agentcore create-memory \
  --memory-name legalai-memory \
  --memory-type CONVERSATION
```

**2. Bedrock Model Access Denied**
```bash
# Request model access in Bedrock console
# Or use CLI to check access
aws bedrock list-foundation-models --region us-east-1
```

**3. Lambda Function Timeout**
```bash
# Increase timeout in CDK stack
timeout: Duration.minutes(5)
```

**4. CORS Issues**
```bash
# Update CORS settings in API Gateway
# Check allowed origins in frontend configuration
```

### Logs and Debugging

**View AgentCore Runtime Logs:**
```bash
aws logs tail /aws/ecs/legalai-agentcore-runtime --follow
```

**View Lambda Function Logs:**
```bash
aws logs tail /aws/lambda/legalai-legal-database --follow
```

**View Frontend Logs:**
```bash
aws logs tail /aws/ecs/legalai-frontend --follow
```

## Performance Optimization

### Scaling Configuration

**AgentCore Runtime Scaling:**
- Auto-scaling based on CPU and memory usage
- Minimum 1 instance, maximum 10 instances
- Target CPU utilization: 70%

**Lambda Concurrency:**
- Reserved concurrency for legal tools
- Provisioned concurrency for frequently used functions

**Database Optimization:**
- DynamoDB on-demand billing
- Global secondary indexes for legal queries
- TTL for temporary session data

### Cost Optimization

**Bedrock Usage:**
- Use Claude Haiku for simple queries
- Cache common legal research results
- Implement request batching

**Storage Optimization:**
- S3 Intelligent Tiering for documents
- Lifecycle policies for old legal files
- Compression for archived documents

## Production Deployment

### Multi-Environment Setup

Deploy to multiple environments:

```bash
# Development
ENVIRONMENT=dev ./deploy.sh

# Staging
ENVIRONMENT=staging ./deploy.sh

# Production
ENVIRONMENT=prod ./deploy.sh
```

### Production Checklist

- [ ] Enable AWS WAF for API protection
- [ ] Configure backup and disaster recovery
- [ ] Set up monitoring and alerting
- [ ] Enable AWS Config for compliance
- [ ] Configure VPC endpoints for security
- [ ] Set up cross-region replication
- [ ] Enable AWS GuardDuty for threat detection
- [ ] Configure AWS Secrets Manager rotation
- [ ] Set up legal document retention policies
- [ ] Enable comprehensive audit logging

### Legal Compliance

**Bar Association Compliance:**
- Review AI assistance guidelines
- Ensure professional responsibility compliance
- Configure appropriate disclaimers
- Set up attorney oversight workflows

**Data Protection:**
- GDPR compliance for EU clients
- CCPA compliance for California clients
- HIPAA compliance if handling health data
- SOX compliance for public companies

## Support and Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Review error logs and performance metrics
- Check legal API key expiration
- Monitor document processing volumes

**Monthly:**
- Update legal database subscriptions
- Review and rotate API keys
- Analyze usage patterns and costs
- Update legal research databases

**Quarterly:**
- Review security configurations
- Update compliance documentation
- Conduct security assessments
- Review legal AI model performance

### Getting Help

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/adianautiyal/LegalAI/issues)
- **Documentation**: [Complete documentation](https://github.com/adianautiyal/LegalAI/wiki)
- **AWS Support**: For AgentCore and Bedrock issues
- **Legal AI Community**: Best practices and discussions

## Next Steps

After successful deployment:

1. **Test with Sample Contracts**: Upload test legal documents
2. **Configure Legal Databases**: Set up access to legal research APIs
3. **Train Your Team**: Provide training on legal AI assistance
4. **Set Up Monitoring**: Configure alerts and dashboards
5. **Plan Scaling**: Prepare for increased usage
6. **Legal Review**: Have legal team review AI assistance workflows

---

For detailed API documentation and advanced configuration options, see the [API Reference](API.md) and [Configuration Guide](CONFIGURATION.md).