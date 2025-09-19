import re
import xml.etree.ElementTree as ET
import csv

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

# CSVに保存
def save_to_csv(fields, output_path):
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['計算フィールド名', '計算式'])
        for field in fields:
            writer.writerow([field['column'], field['calculation']])

def main():

    file_path = input("Tableau（twb）のローカルパスを入力してください: ")
    output_path = input("出力csvのパスを入力してください: ")

    # 計算フィールドを抽出して表示
    calculated_fields = extract_calculated_fields(file_path)

    if calculated_fields:
        save_to_csv(calculated_fields, output_path)
        print("計算フィールドをCSVとして出力しました。")
        print(output_path)
        
    else:
        print("計算フィールドは見つかりませんでした。")


if __name__ == "__main__":
    main()