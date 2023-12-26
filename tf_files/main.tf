terraform {
  backend "gcs" {
    bucket = "tf_state_crypto_strategy"
    prefix = "prod"
  }
}

provider "google" {
    project = var.project_id
    region = var.region
}