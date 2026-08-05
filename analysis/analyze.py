from collections import Counter


def analyze_text_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()

        # Number of characters
        character_count = len(text)

        # Number of words
        word_count = len(text.split())

        # Number of lines
        line_count = len(text.splitlines())

        # Number of unique characters
        unique_characters = len(set(text))

        # Letter frequency (case-insensitive)
        letter_frequency = Counter(
            character.lower()
            for character in text
            if character.isalpha()
        )

        print("\nText Analysis ")
        print(f"File: {filename}")
        print(f"Number of characters: {character_count}")
        print(f"Number of words: {word_count}")
        print(f"Number of lines: {line_count}")
        print(f"Number of unique characters: {unique_characters}")

        print("\nLetter Frequency:")
        for letter in sorted(letter_frequency):
            print(f"{letter}: {letter_frequency[letter]}")

        print(" End of Analysis ")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as error:
        print(f"Error reading file: {error}")


def main():
    filename = "datasets/sample.txt"
    analyze_text_file(filename)


if __name__ == "__main__":
    main()