#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk_python.infra_stack import InfraStackDjango


app = cdk.App()

InfraStackDjango(app, "InfraStack",)

app.synth()
