#!/bin/bash

RESOURCE_GROUP_NAME=ensuring-quality-releases-rg

az deployment group create --resource-group "$RESOURCE_GROUP_NAME" --name deploy-log --template-file log_analytics_template_file.json
