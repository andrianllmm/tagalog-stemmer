import csv
import os
from tabulate import tabulate

from tglstemmer.helpers.words import get_words

from tglstemmer import stemmer


script_dir = os.path.dirname(os.path.realpath(__file__))

valid_words = get_words()


def test_stemmer_accuracy():
    correct = []
    incorrect = []
    results = {
        "accuracy": 0,
        "correct_attempts": 0,
        "incorrect_attempts": 0,
        "understemming_avg": 0,
        "overstemming_avg": 0,
        "understemming_total": 0,
        "overstemming_total": 0,
    }

    examples_file_path = os.path.join(script_dir, "examples.csv")
    correct_file_path = os.path.join(script_dir, "correct.csv")
    incorrect_file_path = os.path.join(script_dir, "incorrect.csv")
    results_file_path = os.path.join(script_dir, "results.csv")

    with open(examples_file_path) as examples_file:
        examples = csv.DictReader(examples_file)

        for example in examples:
            attempt = stemmer.get_stem(example["inflection"])
            example["attempt"] = attempt

            if example["stem"] == attempt:
                correct.append(example)
                results["correct_attempts"] += 1
            else:
                example["in_dictionary"] = example["stem"] in valid_words
                incorrect.append(example)
                results["incorrect_attempts"] += 1

                if len(attempt) > len(example["stem"]):
                    results["understemming_total"] += len(attempt) - len(example["stem"])
                else:
                    results["overstemming_total"] += len(example["stem"]) - len(attempt)

    total_attempts = results["correct_attempts"] + results["incorrect_attempts"]
    if total_attempts > 0:
        results["understemming_avg"] = round(results["understemming_total"] / total_attempts, 2)
        results["overstemming_avg"] = round(results["overstemming_total"] / total_attempts, 2)
        results["accuracy"] = round(results["correct_attempts"] / total_attempts, 4)

    if correct:
        with open(correct_file_path, "w", newline='') as correct_file:
            fieldnames = correct[0].keys()
            writer = csv.DictWriter(correct_file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(correct)

    if incorrect:
        with open(incorrect_file_path, "w", newline='') as incorrect_file:
            fieldnames = incorrect[0].keys()
            writer = csv.DictWriter(incorrect_file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(incorrect)

    with open(results_file_path, "w", newline='') as results_file:
        fieldnames = results.keys()
        writer = csv.DictWriter(results_file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerow(results)

    print(tabulate([results], headers="keys"))


if __name__ == "__main__":
    test_stemmer_accuracy()