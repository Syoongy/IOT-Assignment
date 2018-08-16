import requests
import json

def ocr_space_file(filename, overlay=True, api_key='188ad67f9088957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    imageData = r.json()
    tmpreturnData = imageData['ParsedResults'][0]['TextOverlay']['Lines']
    returnData = []
    for wData in tmpreturnData:
        wordObject = wData['Words']
        fullWord = ''
        for wordData in wordObject:
            fullWord += wordData['WordText']
        returnData.append(fullWord)
    return returnData
