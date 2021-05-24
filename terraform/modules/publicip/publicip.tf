resource "azurerm_public_ip" "test" {
  name                = "${var.webapp_name}-${var.resource_type}-pubip"
  location            = var.location
  resource_group_name = var.resource_group
  allocation_method   = "Dynamic"

  tags = {
    Project = var.project
  }
}
