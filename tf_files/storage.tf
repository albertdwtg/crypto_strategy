
resource "google_storage_bucket" "bucket_historical_data" {
  project                     = var.project_id
  name                        = "${var.resource_prefix}_historical_data"
  force_destroy               = false
  uniform_bucket_level_access = true
  location                    = var.region
}