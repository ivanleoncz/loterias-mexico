import os


def detect_lottery_product(content: str) -> str:
    """
    Detect lottery product and return the filesystem path for the dataset.
    """
    product_number = content.split('\n')[1].split(',')[0]
    if product_number == '60':
        return os.environ["DATASET_PATH_TRIS"]
    elif product_number == '30':
        return os.environ["DATASET_PATH_MELATE_RETRO"]