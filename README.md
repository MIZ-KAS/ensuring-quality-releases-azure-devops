# Ensuring Quality Releases with Azure DevOps
Building a CI/CD pipeline with Azure DevOps.

### Status
[![Build Status](https://dev.azure.com/marcopaspuel/ensuring-quality-releases/_apis/build/status/marcoBrighterAI.azure-devops-ensuring-quality-releases?branchName=main)](https://dev.azure.com/marcopaspuel/ensuring-quality-releases/_build/latest?definitionId=7&branchName=main)

### Introduction

This project uses **Azure DevOps** to build a CI/CD pipeline that creates disposable test environments and runs a variety of
automated tests to ensure quality releases. It uses **Terraform** to deploy the infrastructure, **Azure App Services** to host
the web application and **Azure Pipelines** to provision, build, deploy and test the project. The automated tests run on a self-hosted
virtual machine (Linux) and consist of: **UI Tests** with selenium, **Integration Tests** with postman, **Stress Test** and **Endurance
Test** with jmeter. Additionally, it uses an **Azure Log Analytics** workspace to monitor and provide insight into the application's
behavior.

### Prerequisites
- [Azure Account](https://portal.azure.com) 
- [Azure command line interface](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure DevOps Account](https://dev.azure.com/) 

### Project Dependencies
- [Terraform](https://www.terraform.io/downloads.html)
- [JMeter](https://jmeter.apache.org/download_jmeter.cgi)
- [Postman](https://www.postman.com/downloads/)
- [Python](https://www.python.org/downloads/)
- [Selenium](https://sites.google.com/a/chromium.org/chromedriver/getting-started)



Log into your Azure account
``` bash
    az login 
```

``` bash 
    az account set --subscription="SUBSCRIPTION_ID"
```
Create Service Principle
``` bash
    az ad sp create-for-rbac --name TerraformSP-EQR --role="Contributor" --scopes="/subscriptions/SUBSCRIPTION_ID"
```

Configure the storage account for terraform 
``` bash
    ./config_storage_account.sh
```

Login to the newly created vm
``` bash
    ssh -i ~./ssh/azure_eqr_id_rsa marco@13.69.60.241
    ssh -o "IdentitiesOnly=yes" -i ~/.ssh/azure_eqr_id_rsa marco@40.68.13.148
```
