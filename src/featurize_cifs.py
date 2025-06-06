import os
import glob
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from pymatgen.core import Structure
from matminer.featurizers.composition import Stoichiometry, ElementProperty
from matminer.featurizers.structure import DensityFeatures, RadialDistributionFunction


def featurize_structure(file_path, featurizers):
    try:
        structure = Structure.from_file(file_path)
        features = {}
        for name, featurizer, featurizer_type in featurizers:
            if featurizer_type == "structure":
                feats = featurizer.featurize(structure)
            elif featurizer_type == "composition":
                feats = featurizer.featurize(structure.composition)
            else:
                feats = []
            if isinstance(feats, (list, tuple)):
                for i, val in enumerate(feats):
                    features[f"{name}_{i}"] = val
            else:
                features[name] = feats
        features["filename"] = os.path.basename(file_path)
        return features
    except Exception as e:
        logging.warning(f"Failed to featurize {file_path}: {e}")
        return None


def batch_featurize_cifs_parallel(input_folder, output_csv, log_file, workers):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    cif_files = glob.glob(os.path.join(input_folder, "*.cif"))
    logging.info(f"Found {len(cif_files)} CIF files in {input_folder}")

    featurizers = [
        ("stoichiometry", Stoichiometry(), "composition"),
        ("element_property", ElementProperty.from_preset("magpie"), "composition"),
        ("density", DensityFeatures(), "structure"),
        ("rdf", RadialDistributionFunction(), "structure"),
    ]

    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(featurize_structure, f, featurizers): f for f in cif_files}
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                results.append(res)

    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        logging.info(f"Saved featurized data for {len(results)} files to {output_csv}")
    else:
        logging.warning("No featurization results to save.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch featurize CIF files using matminer.")
    parser.add_argument("--input_folder", required=True, help="Folder with CIF files")
    parser.add_argument("--output_csv", required=True, help="Output CSV file path")
    parser.add_argument("--log_file", required=True, help="Log file path")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    args = parser.parse_args()

    batch_featurize_cifs_parallel(args.input_folder, args.output_csv, args.log_file, args.workers)

