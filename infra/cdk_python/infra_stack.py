from aws_cdk import (
    Stack,
    aws_apprunner as apprunner,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
    aws_iam as iam,
)

from constructs import Construct

import os 
from dotenv import load_dotenv
load_dotenv()

STACK_STAGE = os.getenv('AWS_STAGE')


class InfraStackDjango(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Docker Image Asset
        docker_image = ecr_assets.DockerImageAsset(self, f"{STACK_STAGE}-django-image",
            directory="../",  # Path to Dockerfile
        )

        # Create roles first
        build_role = self._create_apprunner_build_role()
        service_role = self._create_apprunner_service_role()

        # App Runner Service
        apprunner_service = apprunner.CfnService(self, f"{STACK_STAGE}-app-runner",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn=build_role.role_arn
                ),
                auto_deployments_enabled=True,

                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier=docker_image.image_uri,
                    image_repository_type="ECR",
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="8000"  # Django default port
                    )
                )
            ),
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                instance_role_arn=service_role.role_arn  # Add the service role here
            )
        )

    def _create_apprunner_build_role(self):
        """Create role for App Runner to pull from ECR"""
        return iam.Role(self, f"{STACK_STAGE}-AppRunnerBuildRole",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSAppRunnerServicePolicyForECRAccess")
            ]
        )

    def _create_apprunner_service_role(self):
        """Create role for App Runner service execution"""
        return iam.Role(self, f"{STACK_STAGE}-AppRunnerServiceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
            inline_policies={
                "AppRunnerPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                # Add permissions your app needs, for example:
                                "secretsmanager:GetSecretValue",
                                "s3:GetObject",
                                # Add other permissions as needed
                            ],
                            resources=["*"]  # Restrict this to specific resources in production
                        )
                    ]
                )
            }
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "InfraQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
