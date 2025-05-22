# Project ID (can be found on the welcome page of your Google Project)
PROJECT_ID = "longtukoreatranslator"

# The ID of the glossary to retrieve.
GLOSSARY_ID_ALL = "glossary_all"
GLOSSARY_ID_LUNA = "glossary_luna"  # 루나
GLOSSARY_ID_MIGHTY_ARENA = "glossary_mighty_arena"  # 마이티아레나
GLOSSARY_ID_BOSSLAVE = "glossary_bosslave"  # 보스레이브
GLOSSARY_ID_BLAST_M = "glossary_blast_m"  # 블라스트M
GLOSSARY_ID_BLESS = "glossary_bless"  # 블레스
GLOSSARY_ID_SWORD_AND_MAGIC = "glossary_sword_and_magic"  # 검과마법
GLOSSARY_ID_CHEONJON = "glossary_cheonjon"  # 천존
GLOSSARY_ID_KAIROS = "glossary_kairos"  # 카이로스
GLOSSARY_ID_TEA_WANG = "glossary_tea_wang"  # 태왕
GLOSSARY_ID_YULGANG_GLOBAL = "glossary_yulgang_global"  # 열강 global

# A game name to glossary id dict
GLOSSARY_DICT = {
    "全部/전체": GLOSSARY_ID_ALL,
    "루나": GLOSSARY_ID_LUNA,
    "마이티아레나": GLOSSARY_ID_MIGHTY_ARENA,
    "보스레이브": GLOSSARY_ID_BOSSLAVE,
    "블라스트M": GLOSSARY_ID_BLAST_M,
    "블레스": GLOSSARY_ID_BLESS,
    "검과마법": GLOSSARY_ID_SWORD_AND_MAGIC,
    "천존": GLOSSARY_ID_CHEONJON,
    "카이로스": GLOSSARY_ID_KAIROS,
    "太王/태왕": GLOSSARY_ID_TEA_WANG,
    "열강 GLOBAL": GLOSSARY_ID_YULGANG_GLOBAL,
}

# A glossary id to URI dict
GLOSSARY_GCS_URI_DICT = {
    GLOSSARY_ID_ALL: "gs://longtukorea/glossary/glossary_all_20230801.csv",
    GLOSSARY_ID_LUNA: "gs://longtukorea/glossary/루나 용어집.csv",
    GLOSSARY_ID_MIGHTY_ARENA: "gs://longtukorea/glossary/마이티아레나_용어집.csv",
    GLOSSARY_ID_BOSSLAVE: "gs://longtukorea/glossary/보스레이브_용어_0407.csv",
    GLOSSARY_ID_BLAST_M: "gs://longtukorea/glossary/블라스트M_용어_0528.csv",
    GLOSSARY_ID_BLESS: "gs://longtukorea/glossary/블레스_용어집.csv",
    GLOSSARY_ID_SWORD_AND_MAGIC: "gs://longtukorea/glossary/용어집-검과마법 업데이트 번역-180427.csv",
    GLOSSARY_ID_CHEONJON: "gs://longtukorea/glossary/천존_용어집.csv",
    GLOSSARY_ID_KAIROS: "gs://longtukorea/glossary/카이로스 용어집.csv",
    GLOSSARY_ID_TEA_WANG: "gs://longtukorea/glossary/태왕_단가_용어집.csv",
    GLOSSARY_ID_YULGANG_GLOBAL: "gs://longtukorea/glossary/YULGANG GLOBAL.csv",
}

# A tuple(source language, target language) to AutoML model id dict
# (abandoned because Google does not support the model training between Chinese and Korean)
MODEL_DICT = {
    # ("en", "zh-CN"): "NM5b3cf4567b0a18de",
    # ("zh-CN", "en"): "NM9c74a08faa514475",
    # ("en", "zh-TW"): "",
    # ("zh-TW", "en"): "",
    # ("en", "ko"): "NM90e28b1c5cb5180b",
    # ("ko", "en"): "NM167c1faed9f852a4",
    # ("en", "ja"): "",
    # ("ja", "en"): "",
    # ("en", "id"): "",
    # ("id", "en"): "",
    # ("en", "ru"): "",
    # ("ru", "en"): "",
    # ("en", "th"): "",
    # ("th", "en"): "",
}

# the name of the Google private key
PRIVATE_KEY_NAME = "longtukoreatranslator_key.json"
