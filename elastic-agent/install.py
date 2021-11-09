import os
import time
from elastic_agent_setup import ElasticAgent


if __name__ == "__main__":
    # agent = ElasticAgent()
    # verify_ssl = False if os.environ.get('FLEET_ENROLL_INSECURE') else True
    # agent.configure(
    #     os.environ.get('ELASTICSEARCH_USERNAME'),
    #     os.environ.get('ELASTICSEARCH_PASSWORD'),
    #     kibana=os.environ.get('KIBANA_URL'),
    #     elasticsearch=os.environ.get('ELASTICSEARCH_HOSTS'),
    #     force_enroll='--force' if os.environ.get('ENROLL_FORCE') else '',
    #     certificate_authority=os.environ.get('FLEET_CA'),
    #     verify_ssl=verify_ssl
    # )
    # preflight = True if os.environ.get('PREFLIGHT_CHECK') else False
    # agent.install(version=os.environ.get('ELK_VERSION'), preflight_check=preflight)
    verify_ssl = False if os.environ.get('FLEET_ENROLL_INSECURE') else True
    preflight = True if os.environ.get('PREFLIGHT_CHECK') else False
    os.system(f"wget https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{os.environ.get('ELK_VERSION')}-linux-x86_64.tar.gz")
    os.system(f"tar zxvf elastic-agent-{os.environ.get('ELK_VERSION')}-linux-x86_64.tar.gz")
    os.system(f"cd elastic-agent-{os.environ.get('ELK_VERSION')}-linux-x86_64")
    # Installs the elastic-agent, this will fail if you already have a fleet server set up
    os.system(f"/elastic-agent-{os.environ.get('ELK_VERSION')}-linux-x86_64/./elastic-agent install -f --fleet-server-es={os.environ.get('ELASTICSEARCH_HOSTS')} --fleet-server-service-token={os.environ.get('FLEET_SERVER_SERVICE_TOKEN')} --fleet-server-policy={os.environ.get('FLEET_SERVER_POLICY')} --fleet-server-es-ca=/ca.crt --fleet-server-cert=/fleet-server.crt --fleet-server-cert-key=/fleet-server.key --url={os.environ.get('FLEET_URL')} --certificate-authorities=/ca.crt --insecure")
    # Ensures elastic-agent is enrolled, AND pipes the logs so that it can be read by docker
    os.system(f"/usr/bin/elastic-agent enroll -f --fleet-server-es={os.environ.get('ELASTICSEARCH_HOSTS')} --fleet-server-service-token={os.environ.get('FLEET_SERVER_SERVICE_TOKEN')} --fleet-server-policy={os.environ.get('FLEET_SERVER_POLICY')} --fleet-server-es-ca=/ca.crt --fleet-server-cert=/fleet-server.crt --fleet-server-cert-key=/fleet-server.key --url={os.environ.get('FLEET_URL')} --certificate-authorities=/ca.crt --insecure 1>/proc/1/fd/1 2>/proc/1/fd/2 &")
    while True:
        print('Elastic Agent is running .....', flush=True)
        time.sleep(30)
