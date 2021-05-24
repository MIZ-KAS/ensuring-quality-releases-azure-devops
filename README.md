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
- [Azure Command Line Interface](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
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
#### 1. Terraform in Azure
##### 1.1. Create a Service Principal for Terraform
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

##### 1.2. Configure the storage account and state backend
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
You will also need to replace this values in the [azure-pipelines.yaml](azure-pipelines.yaml) file.
```
backendAzureRmResourceGroupName: "RESOURCE_GROUP_NAME"
backendAzureRmStorageAccountName: 'tstate$RANDOM'
backendAzureRmContainerName: 'tstate'
backendAzureRmKey: 'terraform.tfstate'
```
To source this values in your local environment run the following command:
```
source .azure_envs.sh
```
NOTE: The values set in `.azure_envs.sh` are required to run terraform commands from your local environment.
There is no need to run this script if terraform runs in Azure Pipelines.

#### 2. Self-hosted Test Runner and REST API Infrastructure
##### 2.1. Create an SSH key for authentication to a Linux VM in Azure
To generate a public private key pair run the following command (no need to provide a passphrase):
``` bash
cd ~/.ssh/
ssh-keygen -t rsa -b 4096 -f az_eqr_id_rsa
```
Ensure that the keys were created:
``` bash
ls -ll | grep az_eqr_id_rsa
```
For additional information of how to create and use SSH keys, click on the links bellow:
- [Create and manage SSH keys for authentication to a Linux VM in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/create-ssh-keys-detailed)
- [Creating and Using SSH Keys](https://serversforhackers.com/c/creating-and-using-ssh-keys)

##### 2.2. Create a tfvars file to configure Terraform Variables
Create a `terraform.tfvars` file inside the [test](terraform/environments/test) directory and copy the content of the [terraform.tfvars.template](terraform/environments/test/terraform.tfvars.template)
to the newly created file. Change the values based on the outputs of the previous steps.

- The `subscription_id`, `client_id`, `client_secret`, and `tenant_id` can be found in the `.azure_envs.sh` file. 
- Set your desired `location` and `resource_group` for the infrastructure. 
- Ensure that the public key name `vm_public_key` is the same as the one created in step 2.1 of this guide.

##### 2.3. Deploy the REST API infrastructure from your local environment with Terraform
Run Terraform plan 
``` bash
cd terraform/environments/test
```
``` bash
terraform init
```
``` bash
terraform plan -out solution.plan
```
After running the plan you should be able to see all the resources that will be created.

Run Terraform apply to deploy the infrastructure.
``` bash
terraform apply "solution.plan"
```

If everything runs correctly you should be able to see the resources been created. You can also check the creation of 
the resources in the [Azure Portal](https://portal.azure.com/#blade/HubsExtension/BrowseResourceGroups) under 
`Home > Resource groups > "RESOURCE_GROUP_NAME"`

#### 3. Azure DevOps
##### 3.1. Create a new Azure DevOps Project and Service Connections
- a) Go to [Azure DevOps](https://dev.azure.com/)
- b) Click on `New Project`
- c) Give the project a name, a description and click `Create`
- d) Create a new Service Connection `Project settings > Service connections > New service connection`
- e) Inside new service connection select `Azure Resource Manager > Service principal (automatic)`
- f) Select a Resource group, give the connection a name a description and click `Save`.

IMPORTANT: You will need to create two service connections:
- `service-connection-terraform` is created using the same resource group that you provided in step 1.2 of this guide.
- `service-connection-webapp` is created using the resource group that you provided in `terraform.tfvars` file.

A detailed explanation on how to create a new Azure DevOps project and service connection can be found [here](https://www.youtube.com/watch?v=aIvl4NxCWwU&t=253s).

- g) Make sure that the name of the service connections match the names provided in the [azure-pipelines.yaml](azure-pipelines.yaml) file.
``` 
serviceConnectionTerraform: 'service-connection-terraform'
serviceConnectionWebApp: 'service-connection-webapp'
```
- f) Make sure that the webAppName matches the name provided in the `terraform.tfvars` file.

##### 3.2. Add the Self-hosted Test Runner to a Pipelines Environment
- a) Create a New Environment in Azure Pipelines. From inside your project in Azure DevOps go to:
`Pipelines > Environments > New environment`
- b) Give the environment a name e.g. `test`, then select `Virtual machines > Next`.
- c) From the dropdown select `Lunix` and copy the `Registration script`
- d) From a local terminal connect to the Virtual Machine.
Use the ssh key created in step 2.1 of this guide. The public IP can be found in the Azure Portal under
`Home > Resource groups > "RESOURCE_GROUP_NAME" > "Virtual machine"`
``` bash
ssh -o "IdentitiesOnly=yes" -i ~/.ssh/az_eqr_id_rsa marco@PublicIP
```
- e) Once you are logged into the VM paste the `Registration script` and run it.
- f) (optional) Add a tag when promoted.

##### 3.3. Deploy a Log Analytics Workspace
- a) Deploy a new log analytics workspace
Run the [deploy_log_analytics_workspace.sh](analytics/deploy_log_analytics_workspace.sh)
script. Make sure to set a resource group and provide a workspace name when promoted, e.g. `ensuring-quality-releases-log`.
``` bash
cd analytics
./deploy_log_analytics_workspace.sh
```
- b) From a local terminal connect to the Virtual Machine as described above.
- c) Once you are **logged into the VM** run the following commands:
``` bash
wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh
sh onboard_agent.sh -w ${AZURE_LOG_ANALYTICS_ID} -s ${AZURE_LOG_ANALYTICS_PRIMARY_KEY}
sudo /opt/microsoft/omsagent/bin/service_control restart ${AZURE_LOG_ANALYTICS_ID}
```
IMPORTANT: The AZURE_LOG_ANALYTICS_ID and AZURE_LOG_ANALYTICS_PRIMARY_KEY can be found in the [Azure Portal](https://portal.azure.com/#blade/HubsExtension/BrowseResourceGroups).
`Home > Resource groups > "RESOURCE_GROUP_NAME" > "Log Analytics workspace" > Agents management`
They can also be set as secret variables for the pipeline:
`Pipelines > YourPipeline > Edit > Variables > New Variable > put the name and the value and > Save`

##### 3.3. Upload the public SSH key and tfvars to Pipelines Library
- a) Add a secure file to Azure Pipelines. From inside your project in Azure DevOps go to:
`Pipelines > Library > Secure files > + Secure file`
- b) Add the **public ssh key** and the **terraform.tfvars** files to the secure files' library.
- c) Give the pipeline permissions to use the file:
`"SECURE_FILE_NAME" > Authorize for use in all pipelines`

##### 3.4. Create a new Azure Pipeline
- a) From inside your project in Azure DevOps go to:
`Pipelines > Pipelines > Create new pipeline`
- b) Select your project from GitHub
- c) Select `Existing Azure Pipelines YAML file`
- d) Select the `main` branch and select the path to the [azure-pipelines.yaml](azure-pipelines.yaml) file.
- e) Select `Continue` and then `Run pipeline`

If everything goes well you should be able to see the pipeline running throughout the different stages.
