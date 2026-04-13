# Azure Provider source and version being used
terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "=4.1.0"
        }
    }
}



provider "azurerm" {
    features {}
    resource_provider_registrations = "none"
    subscription_id = "3c406ef1-189f-475b-b35d-b9267c08eebb"
}

resource "azurerm_resource_group" "main" {
    name = "assignment-resources"
    location = "West Europe"
}

resource "azurerm_kubernetes_cluster" "main" {
    name = "assignment-aks1"
    location = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name
    dns_prefix = "assignmentaks1"

    default_node_pool {
    name = "default"
    node_count = 1
    vm_size = "Standard_B2als_v2"
    os_disk_size_gb = 30
    }

    identity {
        type = "SystemAssigned"
    }

    tags = {
        Environment = "Dev"
    } 
}

output "client_certificate" {
        value = azurerm_kubernetes_cluster.main.kube_config[0].client_certificate
        sensitive = true
}

output "kube_config" {
    value = azurerm_kubernetes_cluster.main.kube_config_raw
    sensitive = true
}




