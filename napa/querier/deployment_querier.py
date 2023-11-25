from napa.querier.base_querier import Querier


class DeploymentQuerier(Querier):
    def __init__(self):
        super().__init__()

    def get_deployment_replicas(self, namespace, deployment):
        replica = 'kube_deployment_spec_replicas{namespace="' + namespace + '", deployment="' + deployment + '"}'
        result = self.make_query(replica)
        if not result:
            return 0
        return int(result[0]['value'][1])


    def get_deployment_cpu_usage(self, namespace, deployment):
        cpu = 'sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace="' + namespace + '", pod=~"' + deployment + '-.*"})'
        result = self.make_query(cpu)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_cpu_limit(self, namespace, deployment):
        cpu = 'sum(kube_pod_container_resource_limits{container!="istio-proxy", namespace="' + namespace + '", pod=~"' + deployment + '-.*", resource="cpu"})'
        result = self.make_query(cpu)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_mem_usage(self, namespace, deployment):
        mem = 'sum(container_memory_working_set_bytes{cluster="", namespace="' + namespace + '", container!="istio-proxy", image!="", pod=~"' + deployment + '-.*"})'
        result = self.make_query(mem)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_mem_limit(self, namespace, deployment):
        cpu = 'sum(kube_pod_container_resource_limits{container!="istio-proxy", namespace="' + namespace + '", pod=~"' + deployment + '-.*", resource="memory"})'
        result = self.make_query(cpu)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_bw_transmit(self, namespace, deployment):
        bw_tx = 'sum(irate(container_network_transmit_bytes_total{cluster="", namespace="' + namespace + '", pod=~"' + deployment + '-.*"}[5m]))'
        result = self.make_query(bw_tx)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_bw_received(self, namespace, deployment):
        bw_rcv = 'sum(irate(container_network_receive_bytes_total{cluster="", namespace="' + namespace + '", pod=~"' + deployment + '-.*"}[5m]))'
        result = self.make_query(bw_rcv)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_pkt_transmit(self, namespace, deployment):
        pkt_tx = 'sum(irate(container_network_transmit_packets_total{cluster="", namespace="' + namespace + '", pod=~"' + deployment + '-.*"}[5m]))'
        result = self.make_query(pkt_tx)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_deployment_pkt_received(self, namespace, deployment):
        pkt_rvc = 'sum(irate(container_network_receive_packets_total{cluster="", namespace="' + namespace + '", pod=~"' + deployment + '-.*"}[5m]))'
        result = self.make_query(pkt_rvc)
        if not result:
            return 0
        return float(result[0]['value'][1])
