# MA Town Bylaws Project
Stack:
 - s3 (boto3)
 - MongoDB (pymongo)
 - Python 3.12.3
 - bash


### Goals:
 - Scrape:
   - [x] Write a script to scrape ma.gov's website to grab all 351 towns and links to their bylaws
   - [x] write a module to process list and download bylaws files from links
 - MongoDB
   - [x] create db
   - [x] load scrape of ma.gov to collection
   - [x] query and update main collection
 - S3
   - [x] set up bucket
   - [x] save credentials to an `.aws` file
   - [x] save downloads to bucket


### Current findings:
 - 130 out of 349 municipalities/towns in MA use ecode360 to host their bylaws
 - ecode360 looks _very_ scrapeable
 - 
 
  
