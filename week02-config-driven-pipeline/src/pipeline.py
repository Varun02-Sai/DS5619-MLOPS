"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json

import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
  
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    temp=[key for key in REQUIRED_KEYS if key not in config]
    if temp:
        raise ValueError(f"Missing value :{temp}")
    
    return config

    # raise NotImplementedError("load_config is not implemented yet")


def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    
    if fmt  not in ("csv","json"):
        raise ValueError(f"fromt type error other than csv not json: {fmt}")
     
    with open(path,'r')as file :
        if (fmt=="csv"):
            trans=list(csv.DictReader(file))
        else :
            trans=json.load(file)

    if not isinstance(trans,list):
        raise ValueError(f"its not in list form ")
    
    for t in trans:
        if not isinstance(t,dict):
            raise ValueError(f"to be in dict form")
        
        if "amount" not in t or "is_fraud" not in t:
            raise ValueError(f"amount and is_fraud should be in transactions ")
        
        amount =t["amount"]
        if not isinstance(amount,(str,float)) or isinstance(amount ,bool):
            raise ValueError(f"amount to be in str or float format")
        
        is_fraud=t["is_fraud"]:
        if not (isinstance(is_fraud,bool) or isinstance(is_fraud,str ) and is_fraud in ("True","False")):
            raise ValueError(f"is_fraud is to be either bool or str format of ("True","False")")

    return trans

    # raise NotImplementedError("load_transactions is not implemented yet")


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    
    # raise NotImplementedError("run_pipeline is not implemented yet")


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
