.PHONY: ecr-login deploy deploy-hotswap synth diff

# Default values if not set
AWS_REGION ?= us-east-1
AWS_PROFILE ?= default
STACK_NAME ?= InfraStack

# Build the AWS CLI profile argument
PROFILE_ARG := $(if $(AWS_PROFILE),--profile $(AWS_PROFILE),)

# Export these variables so they're available to scripts
export AWS_REGION
export AWS_PROFILE

ecr-login:
	@chmod +x ./scripts/ecr_login.sh
	@./scripts/ecr_login.sh

deploy: ecr-login
	cdk deploy $(STACK_NAME) $(PROFILE_ARG) $(ARGS)

# bypassing CloudFormation in certain cases.
# this might be usefull because we dont use cloudformation
# on the deploy.
deploy-hotswap: ecr-login
	cdk deploy --hotswap $(STACK_NAME) $(PROFILE_ARG) $(ARGS)

synth:
	cdk synth $(STACK_NAME) $(PROFILE_ARG) $(ARGS)

diff:
	cdk diff $(STACK_NAME) $(PROFILE_ARG) $(ARGS)