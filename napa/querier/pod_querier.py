from napa.querier.base_querier import Querier


class PodQuerier(Querier):
    def __init__(self):
        super().__init__()

    def get_pod_cpu_usage(self, namespace, pod_name):
        query_cpu = 'sum(irate(container_cpu_usage_seconds_total{namespace=' \
                    '"' + namespace + '", pod="' + pod_name + '"}[5m])) by (pod)'
        result = self.make_query(query_cpu)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_pod_mem_usage(self, namespace, pod_name):
        query_mem = 'sum(irate(container_memory_working_set_bytes{namespace=' \
                    '"' + namespace + '", pod="' + pod_name + '"}[5m])) by (pod)'
        result = self.make_query(query_mem)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_pod_network_bw_transmit(self, namespace, pod_name):

        query_network_sent = 'sum(rate(container_network_transmit_bytes_total{namespace="' \
                             + namespace + '", pod="' + pod_name + '"}[5m]))'
        result = self.make_query(query_network_sent)
        if not result:
            return 0
        return float(result[0]['value'][1])

    def get_pod_network_bw_received(self, namespace, pod_name):

        query_network_received = 'sum(rate(container_network_receive_bytes_total{namespace="' \
                                 + namespace + '", pod="' + pod_name + '"}[5m]))'
        result = self.make_query(query_network_received)
        if not result:
            return 0
        return float(result[0]['value'][1])
