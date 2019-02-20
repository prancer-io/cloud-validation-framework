vnet_rg = "prod-zah-network-rg"

vnet_name = "zah-prod-vnet-2"
address_space = "172.17.251.64/27"
dns_servers = ["172.17.253.7",
               "172.17.253.8"]

subnet_name = ["default"]
address_prefix = ["172.17.251.64/27"]

location = "eastus"


tags = {
  Department     = "ITS Cloud CoE"
  Environment    = "Sandbox"
  Tier           = "4"
  Owner          = "Paul A Johnson"
  Project        = "Cloud CoE"
  Application    = "ZAHTEST Azure Foundation"
  DataProfile    = ""
  BackupSchedule = ""
  PatchSchedule  = ""
}
