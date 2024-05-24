import json

from validator import *


class JSONValidator:
  def __init__(self, required_validator_schema, required_condition_schema,
               recommended_validator_schema, recommended_condition_schema):
    self.required_validator_schema = required_validator_schema
    self.required_condition_schema = required_condition_schema
    self.recommended_validator_schema = recommended_validator_schema
    self.recommended_condition_schema = recommended_condition_schema

  def read_json(self, file_path: str):
    try:
      with open(file_path, 'r') as file:
        data = json.load(file)
      return data, None
    except Exception as e:
      return None, f"Error reading file: {str(e)}"

  def validate(self, data):
    errors, warnings, values = {}, {}, {}
    # Handle required fields
    self.apply_schema(self.required_validator_schema, self.required_condition_schema, data, errors,
                      warnings, values, True)
    # Handle recommended fields
    self.apply_schema(self.recommended_validator_schema, self.recommended_condition_schema, data,
                      errors, warnings, values, False)
    return errors, warnings, values

  def apply_schema(self, validator_schema, condition_schema, data, errors, warnings, values,
                   is_required):
    for field, validator in validator_schema.items():
      condition = condition_schema.get(field,
                                       "all")  # Default to "all" if no specific condition is set
      if self.should_apply_validation(data, condition):
        if field not in data and is_required:
          errors[field] = "Missing required parameter"
        elif field in data:
          error, warning = validator.validate(data[field])
          if error:
            errors[field] = error
          if warning:
            warnings[field] = warning
          values[field] = data[field]
        elif not is_required:
          values[field] = "Recommended to be specified"

  def should_apply_validation(self, data, condition):
    if condition == "all":
      return True
    elif isinstance(condition, dict):
      for key, value in condition.items():
        if isinstance(value, list):
          if data.get(key) not in value:
            return False
        elif data.get(key) != value:
          return False
    return True

  def save_json(self, data, file_path):
    with open(file_path, 'w') as file:
      json.dump(data, file, indent=4)


def main():
  required_validator_schema = {
    "ArterialSpinLabelingType": StringValidator(allowed_values=["PASL", "(P)CASL", "PCASL"]),
    "BackgroundSuppression": BooleanValidator(),
    "M0Type": StringValidator(),
    "TotalAcquiredPairs": NumberValidator(min_error=0),
    "AcquisitionVoxelSize": NumberArrayValidator(size_error=3),
    "LabelingDuration": NumberValidator(),
    "PostLabelingDelay": NumberOrNumberArrayValidator(),
    "InversionTime": NumberValidator(min_error=0),
    "BolusCutOffTechnique": StringValidator(),
    "BolusCutOffDelayTime": NumberOrNumberArrayValidator()
  }

  required_condition_schema = {
    "ArterialSpinLabelingType": "all",
    "BackgroundSuppression": "all",
    "M0Type": "all",
    "TotalAcquiredPairs": "all",
    "AcquisitionVoxelSize": "all",
    "LabelingDuration": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "PostLabelingDelay": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "InversionTime": {"ArterialSpinLabelingType": "PASL"},
    "BolusCutOffTechnique": {"ArterialSpinLabelingType": "PASL"},
    "BolusCutOffDelayTime": {"ArterialSpinLabelingType": "PASL"}
  }

  recommended_validator_schema = {
    "BackgroundSuppressionNumberPulses": NumberValidator(min_error_include=0),
    "BackgroundSuppressionPulseTime": NumberArrayValidator(min_error=0),
    "LabelingLocationDescription": StringValidator(),
    "VascularCrushingVENC": NumberOrNumberArrayValidator(min_error_include=0),
    "PCASLType": StringValidator(allowed_values=["balanced", "unbalanced"]),
    "CASLType": StringValidator(allowed_values=["single-coil", "double-coil"]),
    "LabelingDistance": NumberValidator(),
    "LabelingPulseAverageGradient": NumberValidator(min_error=0),
    "LabelingPulseMaximumGradient": NumberValidator(min_error=0),
    "LabelingPulseAverageB1": NumberValidator(min_error=0),
    "LabelingPulseFlipAngle": NumberValidator(min_error=0, max_error_include=360),
    "LabelingPulseInterval": NumberValidator(min_error=0),
    "LabelingPulseDuration": NumberValidator(min_error=0),
    "PASLType": StringValidator(),
    "LabelingSlabThickness": NumberValidator(min_error_include=0)
  }

  recommended_condition_schema = {
    "BackgroundSuppressionNumberPulses": {"BackgroundSuppression": True},
    "BackgroundSuppressionPulseTime": {"BackgroundSuppression": True},
    "LabelingLocationDescription": "all",
    "VascularCrushingVENC": {"VascularCrushing": True},
    "PCASLType": {"ArterialSpinLabelingType": "PCASL"},
    "CASLType": {"ArterialSpinLabelingType": "CASL"},
    "LabelingDistance": "all",
    "LabelingPulseAverageGradient": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "LabelingPulseMaximumGradient": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "LabelingPulseAverageB1": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "LabelingPulseFlipAngle": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "LabelingPulseInterval": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "LabelingPulseDuration": {"ArterialSpinLabelingType": ["PCASL", "CASL"]},
    "PASLType": {"ArterialSpinLabelingType": "PASL"},
    "LabelingSlabThickness": {"ArterialSpinLabelingType": "PASL"}
  }

  json_validator = JSONValidator(required_validator_schema, required_condition_schema,
                                 recommended_validator_schema, recommended_condition_schema)
  data_path = "sub-Sub1_asl_2.json"
  try:
    with open(data_path, 'r') as file:
      data = json.load(file)
  except Exception as e:
    print(f"Error reading file: {str(e)}")
    return

  errors, warnings, values = json_validator.validate(data)

  # Saving the results in separate JSON files
  json_validator.save_json(errors, "errors.json")
  json_validator.save_json(warnings, "warnings.json")
  json_validator.save_json(values, "values.json")


if __name__ == "__main__":
  main()
