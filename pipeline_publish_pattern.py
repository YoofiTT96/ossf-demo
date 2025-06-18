import requests
import click

def retrieve_pattern_data_from_file(path:str):
    try:
        with open(path, 'r') as file:
            content = file.read()
            return content
    except Exception as err:
        print(f"An error occurred {err}")

def send_pattern_to_calm_hub(pattern):
    requests.post("http://localhost:8080/calm/namespaces/ossf2025/patterns", data=pattern, headers={'Content-Type': 'application/json'})

@click.command()
@click.option('-p', help="Path to Pattern file to upload")
def main(p):
    if p is None:
        click.secho("Please provide a path to the pattern you would like to instantiate ⚠️", fg="orange")
    else:
        pattern_contents = retrieve_pattern_data_from_file(p)
        send_pattern_to_calm_hub(pattern_contents)
        click.secho("Pattern successfully uploaded to CALM Hub ✅", fg="green")

if __name__ == "__main__":
    main()