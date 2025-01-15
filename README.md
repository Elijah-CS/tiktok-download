# Download Tik Tok videos from data file
download.py will download the tik tok videos in the FavoriteVideoList secftion of the data file

The downloads will be organized as such

```
download.py
feed/
metadata/
```

feed - The directory where the mp4 files are placed
metadata - Information about each video will be placed

Example:
```
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
$ python download.py data.json
```
Example results
```
feed/
  creator_2021-04-17T14-31-47.mp4
  ...
metadata/
  creator_2021-04-17T14-31-47.csv
  ...
```