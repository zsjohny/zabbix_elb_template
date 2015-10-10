#!/usr/bin/python
import datetime
import sys
from optparse import OptionParser
import boto.ec2.cloudwatch

### Arguments
parser = OptionParser()
parser.add_option("-l", "--load-balancer-name", dest="load_balancer_name",
                help="LoadBalancerName")
parser.add_option("-a", "--access-key", dest="access_key",
                help="AWS Access Key")
parser.add_option("-s", "--secret-key", dest="secret_key",
                help="AWS Secret Access Key")
parser.add_option("-m", "--metric", dest="metric",
                help="AWS cloudwatch metric")
parser.add_option("-r", "--region", dest="region",
                help="AWS region")

(options, args) = parser.parse_args()

if (options.load_balancer_name == None):
    parser.error("-l Load Balancer Name is required")
if (options.access_key == None):
    parser.error("-a AWS Access Key is required")
if (options.secret_key == None):
    parser.error("-s AWS Secret Key is required")
if (options.metric == None):
    parser.error("-m AWS cloudwatch metric is required")
if (options.region == None):
    parser.error("-r AWS region is required")    
###

### Real code
metrics = {"HealthyHostCount":{"type":"float", "value":None},
    "UnHealthyHostCount":{"type":"float", "value":None},
    "RequestCount":{"type":"int", "value":None},
    "Latency":{"type":"float", "value":None},
    "HTTPCode_ELB_4XX":{"type":"int", "value":None},
    "HTTPCode_ELB_5XX":{"type":"int", "value":None},
    "BackendConnectionErrors":{"type":"int", "value":None},
    "SurgeQueueLength":{"type":"int", "value":None},
    "SwapUsage":{"type":"int", "value":None},
    "SpilloverCount":{"type":"int", "value":None}}
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

#get the region
if (options.region == None):
    options.region = 'cn-north-1'
    
for r in boto.ec2.cloudwatch.regions():
   if (r.name == options.region):
      region = r
      break

conn = boto.ec2.cloudwatch.CloudWatchConnection(options.access_key, options.secret_key,region=region)

for k,vh in metrics.items():

    if (k == options.metric):

        try:
                res = conn.get_metric_statistics(60, start, end, k, "AWS/ELB", "Average", {"LoadBalancerName": options.load_balancer_name})
               
        except Exception, e:
                print "status err Error running elb_stats: %s" % e.error_message
                sys.exit(1)
        if(len(res)>0):    
            average = res[-1]["Average"] # last item in result set
        else:
            average = 0

        if vh["type"] == "float":
                metrics[k]["value"] = "%.4f" % average
        if vh["type"] == "int":
                metrics[k]["value"] = "%i" % average

        #print "metric %s %s %s" % (k, vh["type"], vh["value"])
        print "%s" % (vh["value"])
        break
