import os
import re

import pandas as pd
from tqdm import tqdm

INPUT_DIR = "input/"
OUTPUT_DIR = "output/"
LANGUAGE_LIST = ["zh-CN", "zh-TW", "en", "ko", "ja", "th", "pt", "id", "vi"]

df_all = pd.DataFrame()
for dir_path, dir_names, file_names in os.walk(INPUT_DIR):
    for file_name in tqdm(file_names, desc=dir_path):
        if file_name.endswith(".xlsx"):
            # get file path
            file_path = os.path.join(dir_path, file_name)
            # read files
            df = pd.read_excel(file_path)
            languages = [language for language in LANGUAGE_LIST if language in df.columns]
            df = df[languages]
            # tag the source file
            df["source"] = file_name
            # combine the output file path
            output_file = re.sub(INPUT_DIR, OUTPUT_DIR, file_path)
            output_file = re.sub(".xlsx", ".csv", output_file)
            # create directory
            output_directory = os.path.dirname(output_file)
            os.makedirs(output_directory, exist_ok=True)
            # save
            df.to_csv(output_file, index=False)
            # merge
            df_all = pd.concat([df_all, df], axis=0, ignore_index=True)
    # move column "source" to the end
    df_all["source"] = df_all.pop("source")

# excel文件输出
df_all.to_excel(os.path.join(INPUT_DIR, "../glossary_all.xlsx"), index=False)
# csv文件输出
df_all.to_csv(os.path.join(INPUT_DIR, "../glossary_all.csv"), index=False)
