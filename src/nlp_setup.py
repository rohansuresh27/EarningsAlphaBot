import nltk
import os

def initialize_nltk():
    """Initialize NLTK by downloading required datasets."""
    try:
        # Set NLTK data path to a writable location
        nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        nltk.data.path.insert(0, nltk_data_dir)

        # Required datasets
        required_datasets = [
            ('punkt', 'tokenizers/punkt'),
            ('averaged_perceptron_tagger', 'taggers/averaged_perceptron_tagger')
        ]

        for dataset, path in required_datasets:
            try:
                nltk.data.find(path)
            except LookupError:
                print(f"Downloading {dataset}...")
                nltk.download(dataset, download_dir=nltk_data_dir)

        return True
    except Exception as e:
        print(f"Failed to initialize NLTK: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_nltk()