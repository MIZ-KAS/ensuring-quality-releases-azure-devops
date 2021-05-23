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

### Getting Started

1. Fork and clone this repository in your local environment
2. Open the project on your favorite text editor or IDE
3. Log into the [Azure Portal](https://portal.azure.com)
4. Log into [Azure DevOps](https://dev.azure.com/)

### Installation & Configuration
#### Terraform in Azure
##### 1. Create a Service Principal for Terraform
Log into your Azure account
``` bash
az login 
```
``` bash 
az account set --subscription="SUBSCRIPTION_ID"
```
Create Service Principle
``` bash
az ad sp create-for-rbac --name ensuring-quality-releases-sp --role="Contributor" --scopes="/subscriptions/SUBSCRIPTION_ID"
```
This command will output 5 values:
``` json
{
  "appId": "00000000-0000-0000-0000-000000000000",
  "displayName": "azure-cli-2017-06-05-10-41-15",
  "name": "http://azure-cli-2017-06-05-10-41-15",
  "password": "0000-0000-0000-0000-000000000000",
  "tenant": "00000000-0000-0000-0000-000000000000"
}
``` 
Create an `.azure_envs.sh` file inside the project directory and copy the content of the `.azure_envs.sh.template` to the newly created file.
Change the parameters based on the output of the previous command. These values map to the `.azure_envs.sh` variables like so:

    appId is the ARM_CLIENT_ID
    password is the ARM_CLIENT_SECRET
    tenant is the ARM_TENANT_ID

##### 2. Configure the storage account and state backend
To [configure the storage account and state backend](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage)
run the bash script [configure_terraform_storage_account.sh](configure_terraform_storage_account.sh) providing
a resource group name, and a desired location. 
``` bash 
./configure_terraform_storage_account.sh -g "RESOURCE_GROUP_NAME" -l "LOCATION"
```
This script will output 3 values:
``` bash 
storage_account_name: tstate$RANDOM
container_name: tstate
access_key: 0000-0000-0000-0000-000000000000
```
Replace the `RESOURCE_GROUP_NAME` and `storage_account_name` in the [terraform/environments/test/main.tf](terraform/environments/test/main.tf)
file and the `access_key` in the `.azure_envs.sh` script.
```
terraform {
    backend "azurerm" {
        resource_group_name  = "RESOURCE_GROUP_NAME"
        storage_account_name = "tstate$RANDOM"
        container_name       = "tstate"
        key                  = "terraform.tfstate"
    }
}
```
```
export ARM_ACCESS_KEY="access_key"
```
To source this values in your local environment run the following command:
```
source .azure_envs.sh
```
NOTE: The values set in `.azure_envs.sh` are required to run terraform commands from your local environment.
There is no need to run this script if terraform runs in Azure Pipelines.

#### Azure DevOps
##### 1. Create an SSH keys for authentication to a Linux VM in Azure
To generate a public private key pair run the following command (no need to provide a pass phase):
``` bash
ssh-keygen -t rsa -b 4096 -f az_eqr_id_rsa
```
Go to your ssh directory and ensure that the keys were created:
``` bash
cd ~/.ssh/
ls -ll | grep az_eqr_id_rsa
```
For additional information of how to create and use SSH keys, click on the links bellow:
- [Create and manage SSH keys for authentication to a Linux VM in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/create-ssh-keys-detailed)
- [Creating and Using SSH Keys](https://serversforhackers.com/c/creating-and-using-ssh-keys)

##### 2. Create a tfvars file to configure Terraform
Create a `terraform.tfvars` file inside the [test](terraform/environments/test) directory and copy the content of the [terraform.tfvars.template](terraform/environments/test/terraform.tfvars.template)
to the newly created file. Change the values based on the outputs of the previous steps.

##### 3. Create a new Azure DevOps Project
A detailed explanation on how to create a new Azure DevOps project can be found [here](https://www.youtube.com/watch?v=aIvl4NxCWwU&t=253s).



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
