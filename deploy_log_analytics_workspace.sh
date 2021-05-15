#!/bin/bash

az deployment group create --resource-group tf-udacity-project3-rg --name deploy-log --template-file deploy_log_analytics_workspace.json
