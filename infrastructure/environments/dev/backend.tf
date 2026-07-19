terraform {
  backend "s3" {
    bucket = "project-nexus-tfstate"
    key    = "dev/terraform.tfstate"
    region = "ap-south-1"
  }
}