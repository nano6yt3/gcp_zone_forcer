import argparse
import subprocess

def create_dns_zone(zone_name, dns_name):
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
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a DNS zone in GCP.")
    parser.add_argument("--zone-name", required=True, help="The name of the DNS zone.")
    parser.add_argument("--dns-name", required=True, help="The DNS name for the zone.")

    args = parser.parse_args()
    create_dns_zone(args.zone_name, args.dns_name)
