import argparse
import subprocess

def create_dns_zone(zone_name, dns_name, ns_match, verbose=False):
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

    try:
        subprocess.run(command, check=True)
        print(f"DNS zone '{zone_name}' with DNS name '{dns_name}' created successfully.")

        # Get the NS records for the newly created zone
        describe_command = ["gcloud", "dns", "managed-zones", "describe", zone_name]
        describe_output = subprocess.check_output(describe_command, universal_newlines=True)

        # Print all the assigned name servers if verbose mode is enabled
        if verbose:
            print("\nAssigned Name Servers:")
            print(describe_output)

        # Check if any of the lines contain the provided NS match
        if ns_match.lower() in describe_output.lower():
            print("Success.")
        else:
            print("No matching NS records found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a DNS zone in GCP.")
    parser.add_argument("--zone-name", required=True, help="The name of the DNS zone.")
    parser.add_argument("--dns-name", required=True, help="The DNS name for the zone.")
    parser.add_argument("--ns-match", required=True, help="The NS record to match.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print all assigned name servers.")

    args = parser.parse_args()
    create_dns_zone(args.zone_name, args.dns_name, args.ns_match, args.verbose)
