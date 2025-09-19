import re
import xml.etree.ElementTree as ET

# formula内の[Calculation_xxx]をフィールド名に置換
def replace_calculation_fields(name, calculation):
    pattern = r'\[Calculation_\w+\]'
    replaced_calculation = re.sub(pattern, r'[' + name + ']', calculation)
    return replaced_calculation

# XMLからCaptionとFormulaを取得
def extract_calculated_fields(file_path):
    
    tree = ET.parse(file_path)
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

    file_path = input("ローカルパス(.twb)を入力してください: ")

    # 計算フィールドを抽出して表示
    calculated_fields = extract_calculated_fields(file_path)

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