import os
import threading
import time
import numpy as np
import pandas as pd
from lib.querier.deployment_querier import DeploymentQuerier
from lib.utils.logger import set_logger

logger = set_logger(__name__)


class ThreadQuerier:
    dataStruct = {
        'Latency': [],
        'CPU_USAGE': [],
        'MEM_USAGE': [],
        'LOAD': [],
        'CONF': []
    }

    def __init__(self):
        # Init thread
        self.thread_run = True
        self.dataFrame = pd.DataFrame(self.dataStruct)
        self.watcher_thread = threading.Thread(target=self.run())

    def run(self):
        start_time = time.time()
        i = 0
        while self.thread_run:
            try:
                myquery = DeploymentQuerier()
                # FIND BENCHY CONF
                cpu_limit = myquery.get_deployment_cpu_limit('monitoring', 'benchy')
                mem_limit = myquery.get_deployment_mem_limit('monitoring', 'benchy')
                current_replicas = myquery.get_deployment_replicas('monitoring', 'benchy')
                flag = check_conf(current_replicas, cpu_limit, mem_limit)
                if not flag:
                    print("Flag == False")
                    raise Exception
                # LOAD METRIC
                result = myquery.make_query('locust_requests_num_requests{container="locust-exporter"}')
                load = result[0]['value'][1]
                # CPU_USAGE METRIC
                cpu_usage = myquery.get_deployment_cpu_usage('monitoring', 'benchy')
                cpu_usage = round(float(cpu_usage), 4)
                # MEM_USAGE METRIC
                mem_usage = myquery.get_deployment_cpu_usage('monitoring', 'benchy')
                mem_usage = round(float(mem_usage), 4)
                # LATENCY
                # error in LOCUST EXPORTER
                # locust_requests_current_response_time_percentile_95 gives 0 as result
                result = myquery.make_query("locust_requests_avg_response_time{container='locust-exporter'}")
                latency = result[0]['value'][1]
                latency = round(float(latency), 2)
                # INSERT INTO DATAFRAME
                temp = pd.DataFrame({"Latency": latency, "CPU_USAGE": cpu_usage, "MEM_USAGE": mem_usage, "LOAD": load,
                                     "CONF": os.getenv("CONF")}, index=[0])
                self.dataFrame = pd.concat([self.dataFrame, temp], ignore_index=True)
                print(self.dataFrame)

            except Exception as e:
                logger.error(e)
                logger.info("Retrying in 15 seconds...")
            finally:
                time.sleep(30)
                if (time.time() - start_time) >= 3600:
                    # An hour has passed
                    # Creating CSV
                    print("Creating CSV, an hour has passed")
                    self.dataFrame.to_csv('./csv_dir/csv_metric_data_' + str(i) + '_.csv', sep=',', index=True,
                                          encoding='utf-8')
                    print("CSV has been created: " + 'csv_metric_data_' + str(i) + '_.csv' + "\n\n")
                    i = i + 1
                    start_time = time.time()


def check_conf(current_replicas, cpu_limit, mem_limit):
    match current_replicas:
        case 1:
            # MEM_LIMIT conversion 256 Mebibit to bit
            if cpu_limit == 0.1 and mem_limit == 268435456.0:
                print('CONF 0')
                os.environ["CONF"] = "CONF_0"
                return True
            else:
                print('Error! This configuration of benchy does not exit')
                return False
        case 2:
            # MEM_LIMIT conversion 512Mebibit to bit
            if cpu_limit == 2 * 0.2 and mem_limit == 2 * 536870912.0:
                print('CONF 2')
                os.environ["CONF"] = "CONF_2"
                return True
            else:
                print('Error! This configuration of benchy does not exit')
                return False
        case 3:
            # MEM_LIMIT conversion 256Mebibit to bit
            if cpu_limit == 3 * 0.3 and mem_limit == 3 * 268435456.0:
                print('CONF 3')
                os.environ["CONF"] = "CONF_3"
                return True
            else:
                print('Error! This configuration of benchy does not exit')
                return False
        case _:
            print('Error! This configuration of benchy does not exit')
            return False
