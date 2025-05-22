import os

from google.cloud import translate_v3 as translate

from settings import *


def create_glossary(
        project_id: str,
        input_uri: str,
        glossary_id: str,
        language_code_list: list = ["zh-CN", "ko"],
        timeout: int = 180,
) -> translate.Glossary:
    """
    Create a equivalent term sets glossary. Glossary can be words or
    short phrases (usually fewer than five words).
    https://cloud.google.com/translate/docs/advanced/glossary#format-glossary
    :param project_id:
    :param input_uri:
    :param glossary_id:
    :param language_code_list:
    :param timeout:
    :return:
    """
    client = translate.TranslationServiceClient()

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    location = "us-central1"  # The location of the glossary

    name = client.glossary_path(project_id, location, glossary_id)
    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=language_code_list
    )

    gcs_source = translate.types.GcsSource(input_uri=input_uri)

    input_config = translate.types.GlossaryInputConfig(gcs_source=gcs_source)

    glossary = translate.types.Glossary(
        name=name, language_codes_set=language_codes_set, input_config=input_config
    )

    parent = f"projects/{project_id}/locations/{location}"
    # glossary is a custom dictionary Translation API uses
    # to translate the domain-specific terminology.
    operation = client.create_glossary(parent=parent, glossary=glossary)

    result = operation.result(timeout)
    print(f"Created: {result.name}")
    print(f"Input Uri: {result.input_config.gcs_source.input_uri}")

    return result


def list_glossaries(
        project_id: str
) -> None:
    """List Glossaries.

    Args:
        project_id: The GCP project ID.

    Returns:
        The glossary.
    """
    client = translate.TranslationServiceClient()

    location = "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    # Iterate over all results
    for glossary in client.list_glossaries(parent=parent):
        print(f"Name: {glossary.name}")
        print(f"Entry count: {glossary.entry_count}")
        print(f"Input uri: {glossary.input_config.gcs_source.input_uri}")

        # Note: You can create a glossary using one of two modes:
        # language_code_set or language_pair. When listing the information for
        # a glossary, you can only get information for the mode you used
        # when creating the glossary.
        for language_code in glossary.language_codes_set.language_codes:
            print(f"Language code: {language_code}")
        print()


def get_glossary(
        project_id: str,
        glossary_id: str
) -> translate.Glossary:
    """Get a particular glossary based on the glossary ID.

    Args:
        project_id: The GCP project ID.
        glossary_id: The ID of the glossary to retrieve.

    Returns:
        The glossary.
    """
    client = translate.TranslationServiceClient()

    name = client.glossary_path(project_id, "us-central1", glossary_id)

    response = client.get_glossary(name=name)
    print(f"Glossary name: {response.name}")
    print(f"Entry count: {response.entry_count}")
    print(f"Input URI: {response.input_config.gcs_source.input_uri}")

    return response


def delete_glossary(
        project_id: str,
        glossary_id: str,
        timeout: int = 180,
) -> translate.Glossary:
    """Delete a specific glossary based on the glossary ID.

    Args:
        project_id: The ID of the GCP project that owns the glossary.
        glossary_id: The ID of the glossary to delete.
        timeout: The timeout for this request.

    Returns:
        The glossary that was deleted.
    """
    client = translate.TranslationServiceClient()

    name = client.glossary_path(project_id, "us-central1", glossary_id)

    operation = client.delete_glossary(name=name)
    result = operation.result(timeout)
    print(f"Deleted: {result.name}")

    return result


if __name__ == '__main__':
    # 设置环境变量
    private_key_path = os.path.abspath("../front/longtukoreatranslator_key.json")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key_path
    list_glossaries(PROJECT_ID)  # 列出术语表
    # get_glossary(PROJECT_ID, GLOSSARY_ID_ALL)  # 获取有关术语表的信息
    # delete_glossary(PROJECT_ID, GLOSSARY_ID_TEA_WANG)  # 删除术语表（list_glossaries操作中，Name中最后一个下划线后的就是glossary_id）
    # create_glossary(PROJECT_ID, INPUT_URI_GCS, GLOSSARY_ID_TEA_WANG, ["zh-CN", "ko"])  # 创建术语表（高级版）
    # for glossary_id, gcs_uri in GLOSSARY_GCS_URI_DICT.items():
    #     delete_glossary(PROJECT_ID, glossary_id)
    #     create_glossary(PROJECT_ID, gcs_uri, glossary_id, ["zh-CN", "ko"])
