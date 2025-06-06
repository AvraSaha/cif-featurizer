# Project Title

CIF Featurizer Project

This project automates the process of featurizing crystal structures from CIF files using Matminer and Pymatgen. It includes batch featurization, data cleaning, and visualization of the features to assist materials science research and machine learning model development.




## Features

- Batch processing of multiple CIF files to extract comprehensive structural and compositional features.
- Data cleaning to handle missing values and improve feature quality.
- Visualizations of feature distributions for exploratory data analysis.
- Modular pipeline design with separate scripts for featurization, cleaning, and visualization.
- Easy to run and customize.


## Installation
Prerequisites:

- Python 3.8 or higher
- pip package manager

## Install Dependencies:

```
pip install -r requirements.txt

``` 
## Usage

- Unzip the data.zip file
- After unzipping you will get two sub-folders named raw and processed
- Place your raw CIF files in the folder: data/raw/
- Run the pipeline by executing following command in the root folder:
```
python3 main.py

``` 
- Output:
   - Processed csv file is saved in: data/processed/
   - Feature distribution plots are saved in: results/plots/
   - Logs are saved in: results/logs/

## Configuration
Modify `main.py` to adjust:
- Input and output file paths
- Number of parallel workers for featurization
- Data cleaning parameters such as NaN thresholds and fill methods



## Contributing
Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests to improve the project

Please follow standard Python coding conventions.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
Created by Avra — feel free to reach out for questions or collaboration!

Email: avrasaha97@gmail.com

