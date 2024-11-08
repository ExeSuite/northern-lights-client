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
Please specify `https://oncosweep-us-northern-lights.pharusdx.com` as the `--url` for the current release. For the `--key`, please contact Ping-Han Hsieh (pinghanh@pharusdx.com) or Timmy Hsieh(timmyhsieh@pharusdx.com).


## Analysis
The OncoSweep™ analysis consists of three key steps:
1. Data Upload
2. Quantification
3. Prediction

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

### Data Annotation
After uploading FASTQ files and creating the experiment, you can annotate samples with a custom annotation file using the command:
```
python app.py annotate --name <EXPERIMENT_NAME> --annotation-file <ANNOTATION_FILE>
```
To enable CA19-9-based prediction in OncoSweep™ Pancreas Spotlight, it is required to include CA19-9 levels in the annotation file. This CSV-formatted file should have the first column listing all sample names, and an optional 'CA19-9' column with floating-point values (NA allowed) if CA19-9 data is used for prediction. Here is an example annotation file:
```
Sample ID,CA19-9
Sample_1,12.9
Sample_2,3.0
Sample_3,17.2
Sample_4,-1.0
Sample_5,4.33
```

### Perform Quantification
Runs miRNA quantification on the uploaded data. A notification will be sent to the configured email address once the analysis is completed.
```
python app.py quant --name <EXPERIMENT_NAME>
```

After performing quantification, it enables the prediction and retrieval of quality control metrics.

### Retrieve Quality Control Metrics
```
python app.py qc --name <EXPERIMENT_NAME>
```

### Prediction
Run Oncosweep™ prediction based on miRNA expression obtained from quantification.
```
python app.py predict --name <EXPERIMENT_NAME>
```
Oncosweep™ Pancreas Spotlight also allows for prediction based on miRNA expression and CA19-9 levels (require annotation which contains CA19-9 levels, see [Data Annotation](#data-annotation)).
```
python app.py predict --name <EXPERIMENT_NAME> --with-ca19-9
```
After performing prediction, it enables the retrieval of prediction report.

### Retrieve Prediction Results
To obtain the prediction result based on miRNA expression.
```
python app.py report --name <EXPERIMENT_NAME>
```
To obtain the prediction result based on miRNA expression and CA19-9.
```
python app.py report --name <EXPERIMENT_NAME> --with-ca19-9
```

## Contact
For any issues or questions, please contact:
* Ping-Han Hsieh: pinghanh@pharusdx.com
* Timmy Hsieh: timmyhsieh@pharusdx.com
