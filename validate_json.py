import json
import os
from jsonschema import Draft7Validator

BASEDIR = os.path.abspath(os.path.dirname(__file__))
json_path = os.path.join(BASEDIR, 'task_folder\event')
schema_path = os.path.join(BASEDIR, 'task_folder\schema')

with open('README.md', 'w') as file:
    file.write('')
    file.close()

def get_json_file(json_file):
    with open(json_file, 'r') as file:
        json_data = file.read()
    opened_json = json.loads(json_data)
    return opened_json

def get_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    return schema

def schema_checker(schema, name):
    check_schema = Draft7Validator(schema=Draft7Validator.META_SCHEMA)
    if check_schema.is_valid(schema):
        with open('README.md', 'a') as file:
            file.write(f'Schema {name} is valid\n')
    else:
        for err in check_schema.iter_errors(instance=schema):
            with open('README.md', 'a') as file:
                file.write(err)

for file_name in os.listdir(schema_path):
    data = get_schema(f'task_folder/schema/{file_name}')
    schema_checker(data, file_name)

def validate_instance(instance, validator, output_file):
    errors = list(validator.iter_errors(instance))
    if errors:
        for error in errors:
            output_file.write(f'- {error.message}\n')
    else:
        output_file.write('Valid\n')

def validate_json(output_file):
    for schema_file in os.listdir(schema_path):
        schema = get_schema(f'task_folder/schema/{schema_file}')
        validator = Draft7Validator(schema)
        for json_file in os.listdir(json_path):
            instance = get_json_file(f'task_folder/event/{json_file}')
            output_file.write(f'Json-file: {json_file}, schema: {schema_file}:\n')
            validate_instance(instance, validator, output_file)


with open('README.md', 'a') as output_file:
    validate_json(output_file)