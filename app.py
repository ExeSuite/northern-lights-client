import argparse
import datetime
import os
import uuid

import yaml
import pandas as pd
import requests
import s3fs
from tqdm import tqdm
from typing import Optional

fs = s3fs.S3FileSystem()

contact_message = "Please contact system administrator (pinghanh@pharusdx.com, timmyhsieh@pharusdx.com)"

def parse_arguments() -> argparse.Namespace:

    home_dir = os.path.expanduser("~")
    default_config = os.path.join(home_dir, ".oncosweep.conf")

    parser = argparse.ArgumentParser(
        description="Send requests to perform miRNA quantification and prediction with Oncosweep™ platform."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_init = subparsers.add_parser('init', help="Initialize the program and store the configuration file.")
    parser_init.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to store the configuration file."
    )
    parser_init.add_argument("--key",
        type=str,
        required=True,
        help="API Key to access Oncosweep™ platform."
    )
    parser_init.add_argument(
        "--url", type=str, required=True, help="URL for Oncosweep™ platform."
    )
    parser_init.add_argument(
        "--email", type=str, required=True, help="Email for receiving the notification."
    )

    parser_upload = subparsers.add_parser('upload', help="Upload the FASTQ files")
    parser_upload.add_argument(
        "--name",
        type=str,
        required=False,
        help="Experiment name.",
    )
    parser_upload.add_argument(
        "--fastq-dir",
        type=str,
        required=True,
        help="Data directory with zipped FASTQ files (*.fastq.gz).",
    )
    parser_upload.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to the Oncosweep™ configuration file."
    )

    parser_quant = subparsers.add_parser('quant', help="Perform Quantification")
    parser_quant.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to the Oncosweep™ configuration file."
    )
    parser_quant.add_argument(
        "--name",
        type=str,
        required=True,
        help="Experiment name.",
    )

    parser_pred = subparsers.add_parser('pred', help="Initialize the program")
    parser_pred.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to the Oncosweep™ configuration file."
    )
    parser_pred.add_argument(
        "--name",
        type=str,
        required=True,
        help="Experiment name.",
    )

    parser_list = subparsers.add_parser('list', help="Initialize the program")
    parser_list.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to the Oncosweep™ configuration file."
    )

    parser_download = subparsers.add_parser('download', help="Initialize the program")
    parser_download.add_argument(
        "--config", type=str, required=False, default=default_config, help="Path to the Oncosweep™ configuration file."
    )
    parser_download.add_argument(
        "--name",
        type=str,
        required=True,
        help="Experiment name.",
    )

    args = parser.parse_args()
    return args

def init(config: str, key: str, url: str, email: str) -> None:
    configuration = {
        "key": key,
        "url": url,
        "email": email,
    }
    with open(os.path.realpath(config), 'w') as file:
        yaml.dump(configuration, file)

def read_config(config: str) -> dict[str, str]:
    with open(os.path.realpath(config), 'r') as file:
        return yaml.safe_load(file)

def upload_fastq(url: str, token: str, name: str, fastq_dir: str, chunk_size: int = 10 * 1024 * 1024) -> None:
    matching_files = os.listdir(fastq_dir)
    headers = {
        'Authorization': f'Bearer {token}',
    }
    n_files = 0
    n_uploaded_files = 0
    for file_path in matching_files:
        if file_path.endswith(".fastq.gz"):
            file_path = os.path.realpath(os.path.join(fastq_dir, file_path))
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            n_files += 1
            with open(file_path, 'rb') as file, tqdm(
                desc=file_name,
                total=file_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                upload_id = None
                uploaded = 0
                part_number = 1
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    is_last_chunk = 'true' if uploaded + len(chunk) >= file_size else 'false'
                    data = {
                            'filename': file_name,
                            'offset': uploaded,
                            'total_size': file_size,
                            'part_number': part_number,
                            'is_last_chunk': is_last_chunk,
                            'name': name
                    }
                    if upload_id:
                        data['upload_id'] = upload_id
                    response = requests.post(
                        url,
                        files={'file': (file_name, chunk)},
                        headers=headers,
                        data=data,
                    )
                    response_data = response.json()
                    if 'upload_id' in response_data:
                        upload_id = response_data['upload_id']

                    if response.status_code != 200:
                        print(response.text)
                        print(f"Failed to upload chunk of {file_name} ({n_uploaded_files+1}/{n_files}). Status code: {response.status_code}. {contact_message}")
                        return

                    uploaded += len(chunk)
                    progress_bar.update(len(chunk))
            n_uploaded_files += 1
    print(f"Upload FASTQ complete successfully ({n_uploaded_files}/{n_files}).")


def send_post_request(url: str, name: str, email: str, token: str) -> Optional[requests.Response]:
    # Define the headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # If no data is provided, use an empty dictionary
    data = {
        "name": name,
        "email": email
    }
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the response
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}. {contact_message}")
        return None


args = parse_arguments()
if args.command.lower() == 'init':
    init(config=args.config, key=args.key, url=args.url, email=args.email)
else:
    config = read_config(args.config)
    if args.command.lower() == 'upload':
        experiment_name = (
            args.name
            if args.name
            else f'{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{uuid.uuid4()}'
        )
        upload_fastq(url=f"{config['url']}/api/upload", token=config['key'], name=experiment_name, fastq_dir=args.fastq_dir)


#datasheet_s3_path = upload_fastq_to_s3(name, fastq_dir)
#send_post_request(url, name, email, token)