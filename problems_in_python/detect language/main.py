import langdetect
from langdetect import detect

def detect_language(text):
    return detect(text)

def main():

    while True:
        text = input("Enter the text in any language to detect the language: ")
        language = detect_language(text)
        print(f"Language detected: {language}")
        choice = input("Do you want to continue? (y/n): ").lower()
        if choice != 'y':
            break



if __name__ == '__main__':
    # try こんにちは (Japanese) or Hello (English)
    main()