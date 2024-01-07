# Connect to Exchange Online
Connect-ExchangeOnline -UserPrincipalName your_mailbox@domai.com

# Set the date range for emails to delete
$startDate = Get-Date "01/01/2018"
$endDate = Get-Date "12/31/2019"

# Find and delete emails within the date range
Search-Mailbox -Identity your_mailbox@domai.com -SearchQuery {Received:01/01/2018..12/31/2019} -DeleteContent
