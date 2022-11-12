import os
from pythonping import ping

async def verify_ping(hostname):
    response = os.system("ping " + hostname)
    # Verifying EXIT_STATUS
    #Exit status could be 0, 1 or 2, 
    #and when it is 0, then the ip is active and available, 
    #otherwise, it is inactive
    if response == 0:
        status = True
    else:
        status = False
    context = {
        'response': response,
        'status': status
    }
    return context

async def ping_host(host):
    ping_result = ping(target=host, count=10, timeout=2)
    return {
        'avg_latency': ping_result.rtt_avg_ms,
        'min_latency': ping_result.rtt_min_ms,
        'max_latency': ping_result.rtt_max_ms,
    }