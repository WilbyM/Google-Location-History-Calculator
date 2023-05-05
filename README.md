# Location duration calculator

This script takes .JSON files that are exported from googles timeline feature and then converts them to a CSV file which filters on

- address
- location name (e.g Fairview Hotel Chincoteague
- Hours Spent
- Unique days

Got to https://takeout.google.com/settings/takeout?hl=en&gl=NZ&expflags
Under "Create A New Export" Deselect all options
Search for Location History and tick that
Export all the json files
Create a Directory to store the script in
Create a Directory within that called timeline-json
Put all the XXXX_MONTH.JSONSs into the timeline-json directory
run the Location-history.py script
The CSV will be located in a newly create directory within the script run location
