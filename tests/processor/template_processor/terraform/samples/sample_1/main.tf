
variable "vnet_name" {
    default = "prancer-vnet"
}

variable "vnet_rg" {
    default = "prancer-test-rg"
}

variable "address_space" {
    default = "10.254.0.0/16"
}

variable "location" {
    default = "eastus2"
}

variable "tags" {
    default = {
        environment = "Production",
        project     = "Prancer"
    }
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  resource_group_name = var.vnet_rg
  address_space       = [var.address_space]
  location            = var.location
  tags                = var.tags
}