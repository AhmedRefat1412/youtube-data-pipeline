import json
from src.fetcher import DataFetcher
from src.transformer import DataTransformer
from src.loader import DataLoader

# الاربع قنوات الي هيجي منهم الداتا 
CHANNEL_IDS = [
    "UCJUCcJUeh0Cz2xyKwkw5Q1w",  # beinSpots
    "UCLiTe0aOHShx7hXGyqZ9UIw",  # Nat Geo Abu Dhabi
    "UCe6eisvsctSPvBhmincn6kA",  # JoeHattab
    "UC16niRr50-MSBwiO3YDb3RA",  # BBCNews
]

def main():
    #  1: Ingestion
    print("=== Step 1: Fetching Data ===")
    fetcher = DataFetcher()
    raw_data = fetcher.fetch_all(CHANNEL_IDS)
    print(f"Total videos fetched: {len(raw_data)}")

    # 2:  Transformation
    print("\n=== Step 2: Transforming Data ===")
    transformer = DataTransformer()
    videos, comments = transformer.transform_all(raw_data)

    #  3: Loading
    print("\n=== Step 3: Loading Data ===")
    loader = DataLoader()
    loader.create_tables()
    loader.load_videos(videos)
    loader.load_comments(comments)
    loader.close()

    print("\n=== Pipeline Complete ===")
    print(f"Videos loaded: {len(videos)}")
    print(f"Comments loaded: {len(comments)}")

if __name__ == "__main__":
    main()