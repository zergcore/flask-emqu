import os
from pythonping import ping

async def verify_ping(hostname):
    response = os.system("ping " + hostname)
    # Verifying EXIT_STATUS
    if response == 0:
        status = "active"
    else:
        status = "inactive"
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