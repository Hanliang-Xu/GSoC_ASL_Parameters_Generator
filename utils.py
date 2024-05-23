from typing import List, Tuple, Any, Dict

# Constants for thresholds and valid types
MIN_PAIRS_WARNING_THRESHOLD = 0
MAX_PAIRS_WARNING_THRESHOLD = 10
MIN_PAIRS_ERROR_THRESHOLD = -1
MAX_PAIRS_ERROR_THRESHOLD = 100
VOXEL_SIZE_MIN_WARNING_THRESHOLD = 1
VOXEL_SIZE_MAX_WARNING_THRESHOLD = 10
VOXEL_SIZE_MIN_ERROR_THRESHOLD = 0
VOXEL_SIZE_MAX_ERROR_THRESHOLD = 100
VALID_ASL_TYPES = ["PASL", "PCASL", "(P)CASL", "Velocity-selective"]

MIN_LABELING_DURATION_WARNING = 1
MAX_LABELING_DURATION_WARNING = 10
MIN_LABELING_DURATION_ERROR = 0
MAX_LABELING_DURATION_ERROR = 100
MIN_POST_LABELING_DELAY_WARNING = 1
MAX_POST_LABELING_DELAY_WARNING = 10
MIN_POST_LABELING_DELAY_ERROR = 0
MAX_POST_LABELING_DELAY_ERROR = 100

MIN_INVERSION_TIME_ERROR_THRESHOLD = 0

def validate_asl_type(asl_type: str) -> Tuple[List[str], List[str], str]:
  """Validate arterial spin labeling type."""
  errors = []
  warnings = []
  if asl_type not in VALID_ASL_TYPES:
    errors.append(
      f"Invalid 'ArterialSpinLabelingType': {asl_type}. Expected one of {VALID_ASL_TYPES}")
  return errors, warnings, asl_type


def validate_background_suppression(bs: Any) -> Tuple[List[str], List[str], str]:
  """Validate background suppression."""
  errors = []
  warnings = []
  if bs not in [True, False]:
    errors.append("Missing or invalid 'BackgroundSuppression' (should be True or False)")
  return errors, warnings, "Yes" if bs else "No"


def validate_m0b_method(m0b_method: str) -> Tuple[List[str], List[str], str]:
  """Validate method for M0b estimation."""
  errors = []
  warnings = []
  if not m0b_method:
    errors.append("Missing or invalid 'Method for M0b estimation'")
  return errors, warnings, m0b_method


def validate_total_pairs(total_pairs: int) -> Tuple[List[str], List[str], int]:
  """Validate total acquired pairs."""
  errors = []
  warnings = []
  if total_pairs < MIN_PAIRS_ERROR_THRESHOLD or total_pairs > MAX_PAIRS_ERROR_THRESHOLD:
    errors.append(
      f"'TotalAcquiredPairs' out of valid range ({MIN_PAIRS_ERROR_THRESHOLD}-{MAX_PAIRS_ERROR_THRESHOLD})")
  elif total_pairs == 0 or total_pairs > MAX_PAIRS_WARNING_THRESHOLD:
    warnings.append("'TotalAcquiredPairs' is 0 or greater than 10, which may be unusual")
  return errors, warnings, total_pairs


def validate_voxel_size(voxel_size: List[int]) -> Tuple[List[str], List[str], List[int]]:
  """Validate acquisition voxel size."""
  errors = []
  warnings = []
  if not isinstance(voxel_size, list) or len(voxel_size) != 3:
    errors.append("Invalid 'AcquisitionVoxelSize' (should be a list of 3 numbers)")
  else:
    for size in voxel_size:
      if size < VOXEL_SIZE_MIN_ERROR_THRESHOLD or size > VOXEL_SIZE_MAX_ERROR_THRESHOLD:
        errors.append("'AcquisitionVoxelSize' out of valid range (0-100)")
      elif size < VOXEL_SIZE_MIN_WARNING_THRESHOLD or size > VOXEL_SIZE_MAX_WARNING_THRESHOLD:
        warnings.append("'AcquisitionVoxelSize' is in a warning range (0-1 or 10-100)")
  return errors, warnings, voxel_size


def validate_recommended_parameters(data: Dict[str, Any]) -> Tuple[
  List[str], List[str], Dict[str, Any]]:
  """Validate recommended parameters from the JSON data."""
  errors, warnings = [], []
  values = {}

  if data.get("BackgroundSuppression"):
    values["NumberOfBackgroundSuppressionPulses"] = data.get("BackgroundSuppressionNumberPulses",
                                                             "Not provided")
    values["BackgroundSuppressionPulseTiming"] = data.get("BackgroundSuppressionPulseTime",
                                                          "Not provided")
    values["BackgroundSuppressionTimingDefinition"] = data.get(
      "BackgroundSuppressionTimingDefinition", "Not provided")
  else:
    values["NumberOfBackgroundSuppressionPulses"] = "Not applicable"
    values["BackgroundSuppressionPulseTiming"] = "Not applicable"
    values["BackgroundSuppressionTimingDefinition"] = "Not applicable"

  values["LabelingLocationDescription"] = data.get("LabelingLocationDescription", "Not provided")
  values["ShimVolume"] = data.get("ShimVolume", "Not provided")

  if data.get("VascularCrushing"):
    values["Venc"] = data.get("Venc", "Not provided")
    values["b"] = data.get("b", "Not provided")
  else:
    values["Venc"] = "Not applicable"
    values["b"] = "Not applicable"

  return errors, warnings, values


def validate_labeling_duration(labeling_duration: float) -> Tuple[List[str], List[str], float]:
  """Validate labeling duration."""
  errors = []
  warnings = []
  if labeling_duration < MIN_LABELING_DURATION_ERROR or labeling_duration > MAX_LABELING_DURATION_ERROR:
    errors.append(
      f"'LabelingDuration' out of valid range ({MIN_LABELING_DURATION_ERROR}-{MAX_LABELING_DURATION_ERROR})")
  elif labeling_duration < MIN_LABELING_DURATION_WARNING or labeling_duration > MAX_LABELING_DURATION_WARNING:
    warnings.append(
      f"'LabelingDuration' is less than {MIN_LABELING_DURATION_WARNING} or greater than {MAX_LABELING_DURATION_WARNING}, which may be unusual")
  return errors, warnings, labeling_duration


def validate_post_labeling_delay(post_labeling_delay: float) -> Tuple[List[str], List[str], float]:
  """Validate post labeling delay."""
  errors = []
  warnings = []
  if post_labeling_delay < MIN_POST_LABELING_DELAY_ERROR or post_labeling_delay > MAX_POST_LABELING_DELAY_ERROR:
    errors.append(
      f"'PostLabelingDelay' out of valid range ({MIN_POST_LABELING_DELAY_ERROR}-{MAX_POST_LABELING_DELAY_ERROR})")
  elif post_labeling_delay < MIN_POST_LABELING_DELAY_WARNING or post_labeling_delay > MAX_POST_LABELING_DELAY_WARNING:
    warnings.append(
      f"'PostLabelingDelay' is less than {MIN_POST_LABELING_DELAY_WARNING} or greater than {MAX_POST_LABELING_DELAY_WARNING}, which may be unusual")
  return errors, warnings, post_labeling_delay


def validate_inversion_time(inversion_time: float) -> Tuple[List[str], List[str], float]:
  """Validate post labeling delay."""
  errors = []
  warnings = []
  if inversion_time <= MIN_INVERSION_TIME_ERROR_THRESHOLD:
    errors.append(
      f"'InversionTime' not greater than {MIN_INVERSION_TIME_ERROR_THRESHOLD}")
  """elif inversion_time < [PLACEHOLDER] or inversion_time > [PLACEHOLDER]:
    warnings.append(
      f"'InversionTime' is less than {[PLACEHOLDER]} or greater than {[PLACEHOLDER]}, which may be unusual")
  """
  return errors, warnings, inversion_time