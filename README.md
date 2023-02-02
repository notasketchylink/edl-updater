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

## Free threat intel sources

URL or Domain based lists

  * AdGuardDNS – https://v.firebog.net/hosts/AdguardDNS.txt
  * EasyList – https://v.firebog.net/hosts/Easylist.txt
  * Mandiant APT1 – https://v.firebog.net/hosts/APT1Rep.txt
  * DigitalSide – https://osint.digitalside.it/Threat-Intel/lists/latesturls.txt
  * DigitalSide – https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt
  * Phishing Army – https://phishing.army/download/phishing_army_blocklist_extended.txt
  * AlienVault – http://reputation.alienvault.com/reputation.data
  * URLHaus – https://urlhaus.abuse.ch/downloads/text_online/

IP based lists

  * opendbl talos – https://opendbl.net/lists/talos.list
  * opendbl emerging – https://opendbl.net/lists/etknown.list
  * opendbl brute force – https://opendbl.net/lists/bruteforce.list
  * opendbl blockde – https://opendbl.net/lists/blocklistde-all.list
  * iplists.firehol.org – https://raw.githubusercontent.com/ktsaou/blocklist-ipsets/master/firehol_level1.netset
  * Emerging Threats – https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt
  * Spamhaus EDROP – https://www.spamhaus.org/drop/edrop.txt
  * Spamhaus DROP – https://www.spamhaus.org/drop/drop.txt
  * Cisco Talos – https://www.talosintelligence.com/documents/ip-blacklist
  * DigitalSide – https://osint.digitalside.it/Threat-Intel/lists/latestips.txt
  * CINSScore – https://cinsscore.com/list/ci-badguys.txt
  * Emerging Threats Compromised IPs – https://rules.emergingthreats.net/blockrules/compromised-ips.txt
  * Feodo Botnet C2 – https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt
  * SSL Blacklist – https://sslbl.abuse.ch/blacklist/sslipblacklist.txt
  * Binary Defense – https://www.binarydefense.com/banlist.txt
  
BOGONs

  * Team Cymru IPv4 fullbogons – https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt
  * Team Cymru IPv6 fullbogons – https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt
