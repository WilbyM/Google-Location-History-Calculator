# Location duration calculator

This script takes .JSON files that are exported from googles timeline feature and then converts them to a CSV file which filters on

- address
- location name (e.g Fairview Hotel Chincoteague
- Hours Spent
- Unique days

1. Got to https://takeout.google.com/settings/takeout?hl=en&gl=NZ&expflags
2. Under "Create A New Export" Deselect all options
3. Search for Location History and tick that
4. Export all the json files
5. Create a Directory to store the script in
6. Create a Directory within that called timeline-json
7. Put all the XXXX_MONTH.JSONSs into the timeline-json directory
8. run the Location-history.py script
9. The CSV will be located in a newly create directory within the script run location

