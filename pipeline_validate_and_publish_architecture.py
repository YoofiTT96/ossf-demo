import subprocess
import click
import json
import requests

class ArchitectureValidationException(Exception):
    pass

def remove_connection_options(path_to_architecture):
    with open(path_to_architecture, "r") as file:
        content = file.read()
    json_content = json.loads(content)
    new_relationships = [x for x in json_content["relationships"] if 'connection-options' not in x['unique-id']]
    json_content["relationships"] = new_relationships

    with open(path_to_architecture, "w") as file:
        json.dump(json_content, file, indent=2)

def validate(pattern, architecture):
    remove_connection_options(architecture)
    result = subprocess.run([f"calm validate -p {pattern} -a {architecture}"], capture_output=True, text=True, shell=True)
    output = json.loads(result.stdout)
    if(output['hasErrors'] or output['hasWarnings']):
        click.echo("Validation failed for {architecture} ❌. Errors found: \n")
        pretty_json = json.dumps(output, indent=4)
        print(pretty_json)
        raise ArchitectureValidationException()
    else:
        click.echo("Architecture Validated Successfully ✅")

def retrieve_architecture_file(path):
    try:
        with open(path, "r") as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_to_calm_hub(architecture_path):
    architecture = retrieve_architecture_file(architecture_path)

    response = requests.post("http://localhost:8080/calm/namespaces/ossf2025/architectures", data=architecture, headers={'Content-Type': 'application/json'})
    if(response.status_code == 201):
        click.echo("Successfully uploaded architecture to CALM Hub ✅")
    else:
        click.echo("Failed to upload architecture to CALM Hub❌")

@click.command()
@click.option('-p', help="Pattern file to validate against")
@click.option('-a', help="Architecture file to publish")
def main(p, a):
    try:
        validate(p,a)
        upload_to_calm_hub(a)
    except Exception as err:
        pass

if __name__ == "__main__":
    main()