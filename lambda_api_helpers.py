# API docs: https://cloud.lambdalabs.com/api/v1/docs

from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from colorama import Fore, Style
import time
import colorama


colorama.init()

# load .env file
load_dotenv()

api_key = os.getenv('LAMBDA_KEY')
ssh_key_name = os.getenv('LAMBDA_SSH_KEY_NAME')

def query_lambda_api(endpoint):
    response = requests.get(endpoint, 
                        auth=HTTPBasicAuth(api_key, ''))
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        return data
    else:
        print("Error: ", response.status_code)
        print(response)
        return False
    

def get_instance_types():
    endpoint = "https://cloud.lambdalabs.com/api/v1/instance-types"
    data = query_lambda_api(endpoint)

    # Empty lists to store available and unavailable instances
    available_instances = []
    unavailable_instances = []

    # Iterate over each instance in the data
    for instance in data['data'].values():
        name = instance['instance_type']['name']
        price = instance['instance_type']['price_cents_per_hour'] / 100  # convert cents to dollars
        availability = 'Available' if instance['regions_with_capacity_available'] else 'None available'

        # Append instance to the appropriate list
        if availability == 'Available':
            available_instances.append(instance)
        else:
            unavailable_instances.append(instance)

    # Function to print instance details
    def print_instance_details(instance, availability):
        name = instance['instance_type']['name']
        price = instance['instance_type']['price_cents_per_hour'] / 100  # convert cents to dollars
        print(f"Instance: {name}")
        print(f"Price per hour: ${price}")

        # Use colorama to print availability in green or red
        if availability == 'Available':
            print(f"Availability: {Fore.GREEN}{availability}{Style.RESET_ALL}")
        else:
            print(f"Availability: {Fore.RED}{availability}{Style.RESET_ALL}")

        print("------------------------------")

    # Print details of available instances first
    for instance in available_instances:
        print_instance_details(instance, 'Available')

    # Then print details of unavailable instances
    for instance in unavailable_instances:
        print_instance_details(instance, 'None available')

    return data, available_instances


def attempt_instance(target_names, demo=False):
    data, available_instances = get_instance_types()
    print(available_instances)

    # Loop through each target name to see if it's available
    for target_name in target_names:
        if any(instance['instance_type']['name'] == target_name for instance in available_instances):
            print(f"{Fore.GREEN}{Style.BRIGHT}{target_name} found!{Style.RESET_ALL}")

            instance_data = next((instance for instance in available_instances if instance['instance_type']['name'] == target_name), None)
            region_name = instance_data['regions_with_capacity_available'][0]['name'] if instance_data else None

            if demo:
                data = {
                    'region_name': region_name,
                    'instance_type_name': target_name,
                    'ssh_key_names': [ssh_key_name],
                    'demo_name': demo
                }
            else:
                data = {
                    'region_name': region_name,
                    'instance_type_name': target_name,
                    'ssh_key_names': [ssh_key_name]
                }

            endpoint = 'https://cloud.lambdalabs.com/api/v1/instance-operations/launch'
            response = requests.post(endpoint, auth=HTTPBasicAuth(api_key, ''), json=data)
            print(response.json())
            print("Server spinning up... Your instances:")
            data = query_lambda_api("https://cloud.lambdalabs.com/api/v1/instances")
            if data:
                print("Current instances account:", data)

            time.sleep(1)

            return True, target_name  # Return True and the name of the found instance

    print(f"{Fore.RED}{Style.BRIGHT}None of the target instances found.{Style.RESET_ALL}")
    return False, None  # Return False and None if no instances were found


def snipe_instance(instance_names, demo=False):
    got_a_server = False
    found_instance_name = None
    while not got_a_server:
        try:
            got_a_server, found_instance_name = attempt_instance(instance_names, demo)
            time.sleep(2)
            if got_a_server:
                colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
                for i in range(6):
                    print(f"{colors[i]}{Style.BRIGHT}Server {found_instance_name} found!{Style.RESET_ALL}")
                    time.sleep(0.5)
        except Exception as e:
            print(e)
            time.sleep(1)


def get_my_instances():
    data = query_lambda_api("https://cloud.lambdalabs.com/api/v1/instances")
    if data:
        print("Current instances account:", data)
    return data


def terminate_instance(instance_id):
    endpoint = f"https://cloud.lambdalabs.com/api/v1/instance-operations/terminate"
    data = {'instance_ids': [instance_id]}
    response = requests.post(endpoint, auth=HTTPBasicAuth(api_key, ''), json=data)
    print(response.json())


def terminate_all_instances():
    data = get_my_instances()
    if len(data['data']) > 0:
        for instance in data['data']:
            instance_id = instance['id']
            print("Terminating instance:", instance_id)
            input("press enter to continue")
            terminate_instance(instance_id)
            print("Terminate request sent.")

if __name__ == "__main__":
    # uncomment any multiple of instances that you want to hunt for at any given time.
    snipe_instance([
                    #"gpu_1x_a10",
                    #"gpu_1x_a100_sxm4",
                    #"gpu_8x_h100_sxm5",
                    #"gpu_1x_h100_pcie",
                    #"gpu_8x_a100_80gb_sxm4",
                    #"gpu_1x_rtx6000",
                    #"gpu_1x_a100",
                    #"gpu_2x_a100",
                    #"gpu_4x_a100",
                    #"gpu_8x_a100",
                    "gpu_1x_a6000",
                    #"gpu_2x_a6000",
                    #"gpu_4x_a6000",
                    #"gpu_8x_v100",
                    ])
    
    # Get your current instances:
    #get_my_instances()

    # Terminate all your instances:
    #terminate_all_instances()
