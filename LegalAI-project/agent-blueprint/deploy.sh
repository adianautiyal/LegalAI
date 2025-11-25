#!/bin/bash

# LegalAI Agent Deployment Script
# Deploys the complete LegalAI platform with AgentCore integration

set -e

echo "🏛️ Starting LegalAI Agent Deployment..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v aws &> /dev/null; then
        echo "❌ AWS CLI not found. Please install AWS CLI."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker."
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found. Please install Node.js 18+."
        exit 1
    fi
    
    if ! command -v cdk &> /dev/null; then
        echo "❌ AWS CDK not found. Installing..."
        npm install -g aws-cdk
    fi
    
    echo "✅ Prerequisites check completed"
}

# Load environment variables
load_environment() {
    echo "🔧 Loading environment configuration..."
    
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
        echo "✅ Environment loaded from .env file"
    else
        echo "⚠️ No .env file found. Using default configuration."
        
        # Set default values
        export AWS_REGION=${AWS_REGION:-us-east-1}
        export STACK_PREFIX=${STACK_PREFIX:-legalai}
        export ENVIRONMENT=${ENVIRONMENT:-dev}
    fi
    
    echo "📍 Region: $AWS_REGION"
    echo "🏷️ Stack Prefix: $STACK_PREFIX"
    echo "🌍 Environment: $ENVIRONMENT"
}

# Deploy AgentCore Runtime Stack
deploy_runtime_stack() {
    echo "🚀 Deploying AgentCore Runtime Stack..."
    
    cd agentcore-runtime-stack
    
    # Install dependencies
    npm install
    
    # Bootstrap CDK if needed
    cdk bootstrap aws://$(aws sts get-caller-identity --query Account --output text)/$AWS_REGION
    
    # Deploy the stack
    cdk deploy --require-approval never \
        --parameters StackPrefix=$STACK_PREFIX \
        --parameters Environment=$ENVIRONMENT
    
    echo "✅ AgentCore Runtime Stack deployed"
    cd ..
}

# Deploy AgentCore Gateway Stack
deploy_gateway_stack() {
    echo "🌐 Deploying AgentCore Gateway Stack..."
    
    cd agentcore-gateway-stack
    
    # Build Lambda functions
    echo "🔨 Building Lambda functions..."
    ./scripts/build-lambdas.sh
    
    # Install CDK dependencies
    cd infrastructure
    npm install
    
    # Deploy the gateway stack
    cdk deploy --require-approval never \
        --parameters StackPrefix=$STACK_PREFIX \
        --parameters Environment=$ENVIRONMENT
    
    echo "✅ AgentCore Gateway Stack deployed"
    cd ../..
}

# Deploy Main Application Stack
deploy_app_stack() {
    echo "📱 Deploying Main Application Stack..."
    
    cd chatbot-deployment/infrastructure
    
    # Install dependencies
    npm install
    
    # Deploy the application stack
    cdk deploy --require-approval never \
        --parameters StackPrefix=$STACK_PREFIX \
        --parameters Environment=$ENVIRONMENT \
        --parameters AgentCoreRuntimeArn=$(aws cloudformation describe-stacks \
            --stack-name ${STACK_PREFIX}-agentcore-runtime-${ENVIRONMENT} \
            --query 'Stacks[0].Outputs[?OutputKey==`AgentCoreRuntimeArn`].OutputValue' \
            --output text)
    
    echo "✅ Main Application Stack deployed"
    cd ../..
}

# Configure secrets for legal APIs
configure_secrets() {
    echo "🔐 Configuring API secrets..."
    
    # Create placeholder secrets (users should update with real values)
    aws secretsmanager create-secret \
        --name "${STACK_PREFIX}-legal-database-api-key" \
        --description "Legal Database API Key for LegalAI" \
        --secret-string "PLACEHOLDER_KEY" \
        --region $AWS_REGION 2>/dev/null || echo "Secret already exists"
    
    aws secretsmanager create-secret \
        --name "${STACK_PREFIX}-court-records-credentials" \
        --description "Court Records API Credentials" \
        --secret-string '{"api_key":"PLACEHOLDER","jurisdiction":"US"}' \
        --region $AWS_REGION 2>/dev/null || echo "Secret already exists"
    
    echo "⚠️ Please update the secrets in AWS Secrets Manager with real API keys"
    echo "✅ Secrets configuration completed"
}

# Get deployment outputs
get_outputs() {
    echo "📊 Getting deployment outputs..."
    
    # Get CloudFront URL
    CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
        --stack-name ${STACK_PREFIX}-legalai-app-${ENVIRONMENT} \
        --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontURL`].OutputValue' \
        --output text 2>/dev/null || echo "Not available")
    
    # Get API Gateway URL
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name ${STACK_PREFIX}-agentcore-gateway-${ENVIRONMENT} \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
        --output text 2>/dev/null || echo "Not available")
    
    echo ""
    echo "🎉 LegalAI Deployment Completed Successfully!"
    echo "================================================"
    echo "📱 Application URL: $CLOUDFRONT_URL"
    echo "🔗 API Gateway URL: $API_URL"
    echo "🌍 Region: $AWS_REGION"
    echo "🏷️ Environment: $ENVIRONMENT"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Update API keys in AWS Secrets Manager"
    echo "2. Configure legal database access"
    echo "3. Test the application with sample contracts"
    echo "4. Set up monitoring and alerts"
    echo ""
    echo "📚 Documentation: https://github.com/adianautiyal/LegalAI"
    echo "================================================"
}

# Main deployment flow
main() {
    check_prerequisites
    load_environment
    
    echo "🚀 Starting deployment process..."
    
    # Deploy in order
    deploy_runtime_stack
    deploy_gateway_stack
    deploy_app_stack
    configure_secrets
    
    get_outputs
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "runtime")
        check_prerequisites
        load_environment
        deploy_runtime_stack
        ;;
    "gateway")
        check_prerequisites
        load_environment
        deploy_gateway_stack
        ;;
    "app")
        check_prerequisites
        load_environment
        deploy_app_stack
        ;;
    "secrets")
        load_environment
        configure_secrets
        ;;
    "outputs")
        load_environment
        get_outputs
        ;;
    *)
        echo "Usage: $0 [deploy|runtime|gateway|app|secrets|outputs]"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy all components (default)"
        echo "  runtime  - Deploy only AgentCore Runtime"
        echo "  gateway  - Deploy only AgentCore Gateway"
        echo "  app      - Deploy only main application"
        echo "  secrets  - Configure API secrets"
        echo "  outputs  - Show deployment outputs"
        exit 1
        ;;
esac