import datetime
import socket
import ssl

# Example configuration:

# - type: python-monitor
#   scriptFilePath "/usr/local/scripts/tls_cert_plugin.py"
#   domains ["signalfx.com", "github.com", "google.com"]

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def ssl_valid_time_remaining(hostname):
    # get the number of days left in a cert's lifetime
    try:
        expires = ssl_expiry_datetime(hostname)
    except ssl.SSLError:
        return datetime.timedelta(0)
    return expires - datetime.datetime.utcnow()

def run(config, output):
    domains = config.get("domains")
    for domain in domains:
        r = ssl_valid_time_remaining(domain)
        r = r.total_seconds()
        r = int(r) / 86400
        output.send_gauge("days.remaining", r, {"domain": domain, "source": "tls_cert_plugin"})
