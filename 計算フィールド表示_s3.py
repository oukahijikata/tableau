import boto3
import re
import xml.etree.ElementTree as ET
import tempfile

# formula内の[Calculation_xxx]をフィールド名に置換
def replace_calculation_fields(name, calculation):
    pattern = r'\[Calculation_\w+\]'
    replaced_calculation = re.sub(pattern, r'[' + name + ']', calculation)
    return replaced_calculation

# XMLからCaptionとFormulaを取得
def extract_calculated_fields(bucket_name, key):

    # S3内のtwbファイルをtempで開く
    s3 = boto3.client('s3')
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    
    with open(tmp_file.name, 'wb') as f:
        response = s3.download_fileobj(bucket_name, key, f)
    
    tree = ET.parse(tmp_file.name)
    root = tree.getroot()
    
    calculated_fields = []
    
    # XML内から情報を取得
    for column in root.findall('.//column[@caption]'):
        caption = column.get('caption')
        calculation = None
        calculation_element = column.find('calculation')
        if calculation_element is not None:
            calculation = calculation_element.get('formula')
            calculation = replace_calculation_fields(caption, calculation)
            calculated_fields.append({'column': caption, 'calculation': calculation})
    
    return calculated_fields

def main():

    # バケット名とキーをユーザーからの入力で指定
    bucket_name = input("バケット名を入力してください: ")
    key = input("パスを入力してください: ")

    # 計算フィールドを抽出して表示
    calculated_fields = extract_calculated_fields(bucket_name, key)

    if calculated_fields:
        print("\n[計算フィールドの一覧]")
        for field in calculated_fields:
            print("Caption:", field['column'])
            print("Formula:\n", field['calculation'])
            print()
    else:
        print("計算フィールドは見つかりませんでした。")

    return 0

if __name__ == "__main__":
    main()