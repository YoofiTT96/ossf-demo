import requests
import click

def retrieve_pattern_data_from_file(path:str):
    try:
        with open(path, 'r') as file:
            content = file.read()
            return content
    except Exception as err:
        print(f"An error occurred {err}")

def send_pattern_to_calm_hub(pattern, namespace):
    requests.post(f"http://localhost:8080/calm/namespaces/{namespace}/patterns", data=pattern, headers={'Content-Type': 'application/json'})

@click.command()
@click.option('-p', help="Path to Pattern file to upload")
@click.option('-n', help="Namespace to save the pattern to")
def main(p, n):
    if p is None:
        click.secho("Please provide a path to the pattern you would like to publish to CALM Hub ⚠️", fg="yellow")
    else:
        pattern_contents = retrieve_pattern_data_from_file(p)
        send_pattern_to_calm_hub(pattern_contents, n)
        click.secho("Pattern successfully uploaded to CALM Hub ✅", fg="green")

if __name__ == "__main__":
    main()