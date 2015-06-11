zabbix_elb_template
===================

AWS ELB Template for Zabbix

1. place the script "elb_stats.py" at zabbix-server externalscripts folder (https://www.zabbix.com/documentation/2.0/manual/config/items/itemtypes/external), make sure it has execute permission (Ubuntu - /usr/share/zabbix/externalscripts). 
2. Import the template "elb_template.xml".
3. enter you aws credentials in the template's macro section   {$AWS_ACCESS_KEY},  {$AWS_SECRET_KEY} 
4. Attach the above template to the relevant hosts. The zabbix host name must match the load balancer name
