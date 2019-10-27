import json
import requests
import argparse
import re
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Load article text to a json file")
parser.add_argument("input", help="Input filename")
parser.add_argument("output", help="Output filename")

def remove_junk(soup):
    for script in soup(["script", "style"]):
        script.decompose()


def main(input_filename, output_filename):
    input_file = open(input_filename)
    output_file = open(output_filename, 'w+')

    input_json = json.loads(input_file.read())
    input_file.close()

    output_array = []

    for item in input_json:
        try:
            print(f"Getting article {item.get('resolved_url')}")
            res = requests.get(item.get("resolved_url"))
            if res.status_code == 200:
                try:
                    soup = BeautifulSoup(res.content.decode("utf-8"), "html.parser")
                except UnicodeDecodeError:
                    print(f"Oops, can't decode text on {item.get('resolved_url')}")
                    continue
                remove_junk(soup)
                text = soup.get_text()
                item["text"] = re.sub(r'(\n)+', '\n', soup.get_text())
                output_array.append(item)
            else:
                print(f"got response != 200 from {item.get('resolved_url')}")
        except KeyboardInterrupt:
            print(f"saving to file {output_filename}")
            output_file.write(json.dumps(output_array))
            output_file.close()
            exit(0)
    output_file.write(json.dumps(output_array))
    output_file.close()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.input, args.output)
