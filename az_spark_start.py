import redbull.sparklib as sparklib

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os
import datetime
import random
import argparse

import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batch_auth 
import azure.batch.models as batch_models
import azure.storage.blob as blob

# config file path
_config_path = os.path.join(os.path.dirname(__file__), 'configuration.cfg')

if __name__ == '__main__':

    _pool_id = None
    _vm_count = None
    _vm_size = None
    _wait = None

    # parse arguments
    parser = argparse.ArgumentParser(prog="az_spark")

    parser.add_argument("--cluster-id", required=True,
                        help="the unique name of your spark cluster")
    parser.add_argument("--cluster-size", type=int, required=True,
                        help="number of vms in your cluster")
    parser.add_argument("--cluster-vm-size", required=True,
                        help="size of each vm in your cluster")
    parser.add_argument('--wait', dest='wait', action='store_true')
    parser.add_argument('--no-wait', dest='wait', action='store_false')
    parser.set_defaults(wait=True)

    args = parser.parse_args()
    
    print()
    if args.cluster_id is not None:
        _pool_id = args.cluster_id
        print("spark cluster id:      %s" % _pool_id)

    if args.cluster_size is not None:
        _vm_count = args.cluster_size
        print("spark cluster size:    %i" % _vm_count)

    if args.cluster_vm_size is not None:
        _vm_size = args.cluster_vm_size
        print("spark cluster vm size: %s" % _vm_size)

    if args.wait is not None:
        if args.wait == False:
            _wait = False
        print("wait for cluster:      %r" % _wait)


    # Read config file
    global_config = configparser.ConfigParser()
    global_config.read(_config_path)

    # Set up the configuration
    batch_account_key = global_config.get('Batch', 'batchaccountkey')
    batch_account_name = global_config.get('Batch', 'batchaccountname')
    batch_service_url = global_config.get('Batch', 'batchserviceurl')

    # Set up SharedKeyCredentials
    credentials = batch_auth.SharedKeyCredentials(
        batch_account_name,
        batch_account_key)

    # Set up Batch Client
    batch_client = batch.BatchServiceClient(
        credentials,
        base_url=batch_service_url)

    # Set retry policy
    batch_client.config.retry_policy.retries = 5

    # create spark cluster
    sparklib.create_cluster(
        batch_client,
        _pool_id,
        _vm_count,
        _vm_size, 
        _wait)
