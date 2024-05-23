import json
import logging

from utils import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_json(file_path: str) -> Dict[str, Any]:
  """Load JSON file and return its content as a dictionary."""
  try:
    with open(file_path, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    logging.error(f"File not found: {file_path}")
    raise
  except json.JSONDecodeError:
    logging.error(f"Error decoding JSON from file: {file_path}")
    raise


def verify_general_parameters(data: Dict[str, Any]) -> Tuple[List[str], List[str], Dict[str, Any]]:
  """Verify general required parameters from the JSON data."""
  errors, warnings = [], []
  values = {}

  e, w, v = validate_asl_type(data.get("ArterialSpinLabelingType", ""))
  errors.extend(e)
  warnings.extend(w)
  values["ArterialSpinLabelingType"] = v

  e, w, v = validate_background_suppression(data.get("BackgroundSuppression"))
  errors.extend(e)
  warnings.extend(w)
  values["BackgroundSuppression"] = v

  e, w, v = validate_m0b_method(data.get("M0Type", ""))
  errors.extend(e)
  warnings.extend(w)
  values["MethodForM0bEstimation"] = v

  e, w, v = validate_total_pairs(data.get("TotalAcquiredPairs", -1))
  errors.extend(e)
  warnings.extend(w)
  values["TotalAcquiredPairs"] = v

  e, w, v = validate_voxel_size(data.get("AcquisitionVoxelSize", []))
  errors.extend(e)
  warnings.extend(w)
  values["AcquisitionVoxelSize"] = v

  return errors, warnings, values


def verify_PCASL_required_parameters(data: Dict[str, Any]) -> Tuple[List[str], List[str], Dict[str, Any]]:
  """Verify PCASL required parameters from the JSON data."""
  errors, warnings = [], []
  values = {}

  if data.get("ArterialSpinLabelingType") == "PCASL" or data.get("ArterialSpinType") == "(P)CASL":
    labeling_duration = data.get("LabelingDuration", None)

    if labeling_duration is None:
      # Extend the errors list with a new error message if labeling duration is not provided
      errors.append("Required labeling duration parameter for pcasl not provided")
    else:
      e, w, v = validate_labeling_duration(labeling_duration)
      errors.extend(e)
      warnings.extend(w)
      values["LabelingDuration"] = v

    post_labeling_delay = data.get("PostLabelingDelay", None)

    if post_labeling_delay is None:
      # Extend the errors list with a new error message if labeling duration is not provided
      errors.append("Required post labeling delay parameter for pcasl not provided")
    else:
      e, w, v = validate_post_labeling_delay(post_labeling_delay)
      errors.extend(e)
      warnings.extend(w)
      values["PostLabelingDelay"] = v

  else:
    values["LabelingDuration"] = "Not applicable"
    values["PostLabelingDelay"] = "Not applicable"

  return errors, warnings, values

def main():
  file_path = '../json/sub-Sub103_asl.json'
  try:
    data = load_json(file_path)
    gen_errors, gen_warnings, gen_values = verify_general_parameters(data)
    rec_errors, rec_warnings, rec_values = validate_recommended_parameters(data)
    pcasl_errors, pcasl_warnings, pcasl_values = verify_PCASL_required_parameters(data)

    if gen_errors or rec_errors or pcasl_errors:
      logging.error("Errors found:")
      for error in gen_errors + rec_errors + pcasl_errors:
        logging.error(f"  - {error}")
    else:
      logging.info("No errors found in general required and recommended parameters.")

    if gen_warnings or rec_warnings or pcasl_warnings:
      logging.warning("Warnings:")
      for warning in gen_warnings + rec_warnings + pcasl_warnings:
        logging.warning(f"  - {warning}")

    logging.info("General required values extracted:")
    for key, value in gen_values.items():
      logging.info(f"  - {key}: {value}")

    logging.info("General recommended values extracted:")
    for key, value in rec_values.items():
      logging.info(f"  - {key}: {value}")

    logging.info("PCASL required values extracted:")
    for key, value in pcasl_values.items():
      logging.info(f"  - {key}: {value}")

  except Exception as e:
    logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
  main()
