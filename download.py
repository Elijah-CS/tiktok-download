import json
import csv
import pyktok as pyk
from pathlib import Path
import sys
import os
from multiprocessing import Pool

feed_dir = Path("./feed")
feed_dir.mkdir(parents=True, exist_ok=True)

metadata_dir = Path("./metadata")
metadata_dir.mkdir(parents=True, exist_ok=True)

import traceback

def download_video(link, i):
    original_stdout = sys.stdout 
    sys.stdout = open(os.devnull, 'w') 

    try:
        # Download video and metadata
        results = pyk.save_tiktok(link, True, f"{i}.csv", return_fns=True)
        sys.stdout = original_stdout 
        
        if results is None:
            return
    
        metadata_fn = results["metadata_fn"]
        video_fn = results["video_fn"]

        new_metadata_fn = None
        new_video_fn = None

        # Get video author
        with open(metadata_fn) as f:
            reader = csv.DictReader(f)
            # 1 line 
            for line in reader:
                author = line["author_username"]

                if author.startswith("."):
                    author = author[1:]
                
                # Make new filenames
                video_timestamp = line["video_timestamp"]
                video_timestamp = video_timestamp.replace(":", "-")

                new_metadata_fn = Path(metadata_dir, f"{author}_{video_timestamp}.csv")
                new_video_fn = Path(feed_dir, f"{author}_{video_timestamp}.mp4")

        # Move files to new names
        video_file = Path(video_fn)
        video_file.rename(new_video_fn)

        metadata_file = Path(metadata_fn)
        metadata_file.rename(new_metadata_fn)

    except Exception as e:
        sys.stdout = original_stdout 
        print(f"Failed to download -> {link}")
        if "itemInfo" in str(e):
            pass
        elif "Invalid URL" in str(e):
            pass
        else:
            traceback.print_exc()

if len(sys.argv) < 2:
    print("Must supply a tiktok data file")
    print("Example: python download.py data.json")
    exit(1)

data_file = sys.argv[1]
print(f"Reading data found at {data_file}")

with open(data_file) as f:
    data = json.load(f)

favorites = data["Activity"]["Favorite Videos"]["FavoriteVideoList"]

with Pool(15) as pool:

    args = []
    for i, favorite in enumerate(favorites):
        link = favorite["Link"]
        print("#=========================================================")
        print(link)
        args.append((link, i))

    pool.starmap(func=download_video, iterable=args)