resource "azurerm_storage_account" "storageAccount" {
    count                     = var.storage_count
    name                      = var.storage_name
    resource_group_name       = var.storage_rg_name
    location                  = var.location
    account_tier              = var.account_tier
    account_replication_type  = var.replication_type
    enable_https_traffic_only = var.enableSecureTransfer
    allow_blob_public_access  = var.allow_blob_public_access
    tags                      = var.tags
}