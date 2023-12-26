
resource "google_storage_bucket" "raw" {
  project = var.project_id
  name = "raw_test_crypto_strategy"
  force_destroy = false
  uniform_bucket_level_access = true
  location = var.region
}