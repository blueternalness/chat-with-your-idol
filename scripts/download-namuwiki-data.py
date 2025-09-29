# Script for downloading and processing namuwiki data.
from datasets import load_dataset, Dataset
import pprint

dataset = load_dataset("heegyu/namuwiki", split="train")

columns_to_keep = ["title", "text"]
filtered_dataset = dataset.select_columns(columns_to_keep)



target_characters = {
    "노하라 신노스케" : "짱구",
    "코쿠시보" : "코쿠시보", 
    "몽키 D. 루피/특징": "루피", 
    "우즈마키 나루토": "나루토",
    "손오공(드래곤볼)/특징" : "손오공",
    "키부츠지 무잔": "무잔",
}

filtered_dataset = filtered_dataset.filter(
    lambda example: example['title'] in target_characters.keys()
)

# TODO: TBD - Should we extract/parse only personality?
persona_candidates = {}
for data in filtered_dataset:
    character_name = data['title']
    persona_candidates[character_name] = data['text']



