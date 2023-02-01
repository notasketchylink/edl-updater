# edl-updater
With Palo Alto Networks killing off support & upkeep of their minemeld threat feed tool the need arose for something to meet some basic needs unfulfilled needs.

  1) Download threat feeds
  2) Parse them to FQDNs and IP addresses/subnets
  3) Output deduplicated lists

So with the aid of everyone's favorite AI chatbot I put together a trio of python scripts that meet those oh so lofty goals.

Additional features include:

  * Outputing secondary copies of the FQDN and IP lists annotated with the threat feed the entry came from
  * Basic error logging that is only kind of helpful when something doesn't work
  * Rudimentary archiving of logs and raw threat feeds
  
Tested against Python 3.6 and newer on RHEL 8, Ubuntu 22.04, and Windows 11.
