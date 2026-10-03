terraform {
  backend "s3" {
    bucket = "project-nexus-tfstate"
    key    = "dev/terraform.tfstate"
    region = "eu-west-2"
  }
}