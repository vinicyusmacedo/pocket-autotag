import nltk
from nltk import word_tokenize
import argparse
import json

parser = argparse.ArgumentParser(description="Trains a naive bayes classified from the article list")
parser.add_argument("input", help="Input filename")
parser.add_argument("output", help="Output filename")


def main(input_filename, output_filename):
    input_file = open(input_filename)
    output_file = open(output_filename, 'w+')

    input_json = json.loads(input_file.read())
    input_file.close()

    labeled_text = []
    nltk.download('punkt')

    for item in input_json:
        text = item.get("text")
        tags = [tag for tag in item.get("tags")]
        tokens = word_tokenize(text)
        text = nltk.Text(tokens)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.input, args.output)
