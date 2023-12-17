# from napa.querier.base_querier import Querier
from lib.querier.base_querier import Querier


class NodeQuerier(Querier):
    def __init__(self):
        super().__init__()

    def get_node_cpu_usage(self, deployment, name):
        raise NotImplementedError

    def get_node_mem_usage(self, deployment, name):
        raise NotImplementedError

    def get_node_net_usage(self, deployment, name):
        raise NotImplementedError

    def get_node_network_bw_transmit(self, name):
        raise NotImplementedError

    def get_node_network_bw_received(self, name):
        raise NotImplementedError
