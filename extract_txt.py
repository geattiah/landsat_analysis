ans = []

text_file = "/home/gift/Documents/Landsat/2001_data/extracted/2001__output/mtls/LT05_L1GS_046016_20010718_20161210_01_T2_MTL.txt"


with open(text_file) as rf:
    for line in rf:
        line = line.strip()
        if line.startswith("CLOUD_COVER_LAND"):
            ans.append(line)
        
print(ans)