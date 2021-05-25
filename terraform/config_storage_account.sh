#!/bin/bash
# Helper script to configure the storage account and state backend for Terraform

# Reset in case getopts has been used previously in the shell.
OPTIND=1

usage() { echo "Please specify: -g <Resource Group> -l <Location>"; }

# Get and assign the arguments set by the user
while getopts ":g:l:h" opt; do
  case $opt in
  g)
    RESOURCE_GROUP_NAME="$OPTARG"
    ;;
  l)
    LOCATION="$OPTARG"
    ;;
  h)
    usage
    exit
    ;;
  \?)
    echo "Unknown option: -$OPTARG" >&2
    exit 1
    ;;
  :)
    echo "Missing option argument for -$OPTARG" >&2
    exit 1
    ;;
  *)
    echo "Unimplemented option: -$OPTARG" >&2
    exit 1
    ;;
  esac
done

# Check if all the arguments were provided
if [[ -z ${RESOURCE_GROUP_NAME+x} ]]; then echo "Argument RESOURCE_GROUP_NAME (-g) is unset"; usage; exit 1; fi
if [[ -z ${LOCATION+x} ]]; then echo "Argument LOCATION (-l) is unset"; usage; exit 1; fi

# Initialize additional variables
STORAGE_ACCOUNT_NAME=tstate$RANDOM
CONTAINER_NAME=tstate

# Create resource group
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"

# Create storage account
az storage account create --resource-group "$RESOURCE_GROUP_NAME" --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob

# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group "$RESOURCE_GROUP_NAME" --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' -o tsv)

# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key "$ACCOUNT_KEY"

# Print necessary outputs
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"
