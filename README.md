# OncoSweep™ CLI Tool
This CLI tool allows you to interact with the OncoSweep™ platform for miRNA quantification and prediction. You can upload FASTQ files, perform quantification, retrieve QC results, and manage experiments.

## Prerequisites
```
python
pyyaml
requests
tqdm
```


## Installation
Clone the repository and navigate to the project directory.
Install the required dependencies as described above. It is best to manage the dependency through `conda`:
```
conda create -n northern-lights-client python=3.11 pyyaml requests tqdm
conda activate northern-lights-client
```

## Configuration
Before interacting with OncoSweep™, you must initialize the tool by providing your API key, platform URL, and notification email address. This will generate a configuration file (`$HOME/.oncosweep.conf`) that will store your credentials. This can be achieved by the following command:
```
python app.py init --key <API_KEY> --url <PLATFORM_URL> --email <EMAIL>
```
Please specify `http://oncosweep-us-northern-lights.pharusdx.com` as the `--url` for the current release. For the `--key`, please contact Ping-Han Hsieh (pinghanh@pharusdx.com) or Timmy Hsieh(timmyhsieh@pharusdx.com).


## Analysis
The OncoSweep™ analysis consists of three key steps:
1. Data Upload
2. Quantification
3. Retrieving Quality Control Metrics

Please follow these steps in sequence to complete the analysis.

### Data Upload
Upload gzipped FASTQ files to the OncoSweep™ platform. This will automatically create an analysis with specified experiment name. Note that it is recommend to upload at most 50 files at a time in order to ensure sufficient resources.
```
python app.py upload --fastq-dir <FASTQ_DIRECTORY> [--name <EXPERIMENT_NAME>]
```

### Retrieve Experiment Information
Show the information and available actions for each experiment.
```
python app.py list
```
Alternatively, use `column` and `less` for better visualization:
```
python app.py list | column -ts $'\t' | less -S
```

### Perform Quantification
Runs miRNA quantification on the uploaded data. A notification will be sent to the configured email address once the analysis is completed.
```
python oncosweep.py quant --name <EXPERIMENT_NAME>
```

### Retrieve Quality Control Metrics
```
python oncosweep.py qc --name <EXPERIMENT_NAME>
```

## Contact
For any issues or questions, please contact:
* Ping-Han Hsieh: pinghanh@pharusdx.com
* Timmy Hsieh: timmyhsieh@pharusdx.com
