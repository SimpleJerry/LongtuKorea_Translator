# Imports the Google Cloud Translation library
import os

from google.cloud import translate_v3 as translate

from settings import *


# Initialize Translation client
def translate_text(
        text: str = "YOUR_TEXT_TO_TRANSLATE",
        project_id: str = "YOUR_PROJECT_ID",
        source_language_code: str = "SOURCE_LANGUAGE_CODE",
        target_language_code: str = "TARGET_LANGUAGE_CODE",
) -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from Chinese-Simplified to Korean
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response


def translate_text_with_glossary(
        text: str = "YOUR_TEXT_TO_TRANSLATE",
        project_id: str = "YOUR_PROJECT_ID",
        source_language_code: str = "SOURCE_LANGUAGE_CODE",
        target_language_code: str = "TARGET_LANGUAGE_CODE",
        glossary_id: str = "YOUR_GLOSSARY_ID",
) -> translate.TranslateTextResponse:
    """Translates a given text using a glossary.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project that owns the glossary.
        glossary_id: The ID of the glossary to use.

    Returns:
        The translated text.
"""
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    glossary = client.glossary_path(
        project_id, "us-central1", glossary_id  # The location of the glossary
    )
    glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        request={
            "contents": [text],
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "parent": parent,
            "glossary_config": glossary_config,
        }
    )

    # Display the translation for each input text provided
    for translation in response.glossary_translations:
        print(f"Translated text: {translation.translated_text}")

    return response


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 设置环境变量
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(PRIVATE_KEY_NAME)
    # 主程序
    print("Welcome to LongtuKorea Translator! version:{version}".format(version="1.0 beta"))
    print("author:Jerry.Zhang\n")
    mode = input("Pleaser select a translation mode:\n1:中->한\n2:한->中\nselect:")
    if mode == "1":
        while True:
            text = input("请输入待翻译文本:")
            translate_text_with_glossary(text, PROJECT_ID, "zh-CN", "ko", GLOSSARY_ID_ALL)
    elif mode == "2":
        while True:
            text = input("번역할 텍스트를 입력하세요:")
            translate_text_with_glossary(text, PROJECT_ID, "ko", "zh-CN", GLOSSARY_ID_ALL)
    else:
        print("Program ends. Please rerun it.")
        input()

    # text = input("Please enter the text you want to translate into Korean:")
    # translate_text(text, PROJECT_ID, "zh-CN", "ko")  # 翻译文本（高级版）
    # translate_text_with_glossary(text, PROJECT_ID, "zh-CN", "ko", "Luna_glossary")  # 翻译文本_带术语表（高级版）
