import argparse
import subprocess
import time
import atexit

last_created_zone = None

def delete_last_created_zone():
    global last_created_zone
    if last_created_zone:
        print(f"\nCtrl+C detected. Deleting the last created zone '{last_created_zone}'...")
        delete_command = ["gcloud", "dns", "managed-zones", "delete", last_created_zone, "--quiet"]
        subprocess.run(delete_command, check=True)
        print(f"Last created zone '{last_created_zone}' deleted successfully.")

def create_dns_zone(zone_name, dns_name, ns_match, verbose=False):
    global last_created_zone
    attempts = 0

    while True:
        try:
            attempts += 1
            command = [
                "gcloud",
                "dns",
                "managed-zones",
                "create",
                zone_name,
                "--dns-name=" + dns_name,
                "--visibility=public",
                "--description=sto"
            ]
            subprocess.run(command, check=True)
            last_created_zone = zone_name

            # Get the NS records for the newly created zone
            describe_command = ["gcloud", "dns", "managed-zones", "describe", zone_name]
            describe_output = subprocess.check_output(describe_command, universal_newlines=True)

            # Check if any of the lines contain the provided NS match
            if ns_match.lower() in describe_output.lower():
                if verbose:
                    print(f"\nAttempt: {attempts}\nDNS zone '{zone_name}' with DNS name '{dns_name}' created successfully.")
                    print("\nAssigned Name Servers:")
                    print(describe_output)
                    print("Success.")
                else:
                    print("Success.")
                break
            else:
                if verbose:
                    print(f"\nAttempt: {attempts}\nDNS zone '{zone_name}' with DNS name '{dns_name}' created successfully.")
                    print("\nAssigned Name Servers:")
                    print(describe_output)
                print(f"No matching NS records found. Deleting the zone. (Attempt: {attempts})")
                delete_command = ["gcloud", "dns", "managed-zones", "delete", zone_name, "--quiet"]
                subprocess.run(delete_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            exit(1)
        except KeyboardInterrupt:
            delete_last_created_zone()
            print("\nCtrl+C detected. Exiting the script.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a DNS zone in GCP.")
    parser.add_argument("--zone-name", required=True, help="The name of the DNS zone.")
    parser.add_argument("--dns-name", required=True, help="The DNS name for the zone.")
    parser.add_argument("--ns-match", required=True, help="The NS record to match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print all assigned name servers.")

    args = parser.parse_args()

    try:
        atexit.register(delete_last_created_zone)
        create_dns_zone(args.zone_name, args.dns_name, args.ns_match, args.verbose)
    except KeyboardInterrupt:
        pass
