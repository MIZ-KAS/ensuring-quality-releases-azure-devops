# azure-devops-ensuring-quality-releases
This project uses Azure DevOps to build a CI/CD pipeline that creates disposable test environments and runs a variety of automated tests to ensure quality releases.

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
```
