# This is the pepelie of the yolovFly post data analysis


## Preparing the Data and Video table list

Structrues of the working directory:
<pre>
csv
├── 20210408-1.mp4_1_.json
├── 20210408-1.mp4.csv
├── 20210408-2.mp4_1_.json
├── 20210408-2.mp4.csv
...
Video_post
Video_list.csv
</pre>


1. `mkdir csv` for store the result data: `cvs` and `json` files from the yolovFly results.
2. `mkdri Video_post` for storing the results
3. All video names were stored in `Video_list.csv` file with column of video-names and length of the plate in `pixel` and `mm` for scale the length of the video. For example, in video **20210408-1.mp4**, the plate's diameter (petri dish) is **712 pixels** in this video and **39 mm** in real. So, we can know that each picxel in this video is about **0.0547 mm**. On the other hand, the frame of the video is **1920 * 1080** by default.
4. Next arguments is the start of the frame and the end of the frame. (So we can choose a part of the video to have a test)

```bash
head -n 3 Video_list.csv
```

<pre>
20210408-1.mp4	712	39	1268	6000
20210408-2.mp4	712	39	1268	6000
20210408-3.mp4	712	39	1268	6000
</pre>


### Generate a `Video_list.csv`

```python
import os
import pandas as pd

Video_list = [i.replace(".csv", "") for i in os.listdir("csv") if ".csv" in i]
Len_plate = [712,  712, 712, 712, 813, 813, 813, 813, 926, 924, 925, 926, 920, 915, 931, 931, 931, 931, 957, 959, 959, 933, 933, 942]

A = pd.DataFrame([Video_list, Len_plate]).T
A[2]=39
A[3]=1268
A[4]=6000
A.to_csv("Video_list.csv", sep="\t", index=None, header=None)
```

## Turn raw detection data to discreption matrix

Few things before runing the scripts
3. Change few things in the `1_single_fly_run.py`
	- `Len_plate = [712,  712, ...]`
	 a list of diameters (pixel) from each plate (petri dish). So we can calculate the Scale for each videos.
	- `_Plate_len = 39` The true length of the plate (petri dish) in mm
4. You can also change some other argumetns if you like

```bash
python 1_single_fly_run.py
```
