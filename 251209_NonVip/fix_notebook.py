
import json
import os

target_file = '02_Shap_real.ipynb'

try:
    with open(target_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb.get('cells', [])
    modified = False

    for cell in cells:
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            # Search for the cell with font settings
            source_text = "".join(source)
            if "import matplotlib.pyplot as plt" in source_text and "plt.rc('font', family='Malgun Gothic')" in source_text:
                print("Found target cell.")
                
                # We need to construct the new source code.
                # Since we identified the issue is likely sns.set_style overriding font settings,
                # we will reconstruct the beginning of the cell.
                
                new_source_prefix = [
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import platform\n",
                    "\n",
                    "# -------------------------------------------------------\n",
                    "# 1. 한글 폰트 및 그래프 스타일 설정\n",
                    "# -------------------------------------------------------\n",
                    "# Seaborn 스타일을 먼저 설정해야 폰트 설정이 덮어씌워지지 않습니다.\n",
                    "sns.set_style(\"whitegrid\")\n",
                    "\n",
                    "system_name = platform.system()\n",
                    "if system_name == 'Windows':\n",
                    "    plt.rc('font', family='Malgun Gothic')  # 윈도우\n",
                    "elif system_name == 'Darwin':\n",
                    "    plt.rc('font', family='AppleGothic')    # 맥\n",
                    "else:\n",
                    "    # 코랩(Colab) 등의 리눅스 환경이라면 나눔글꼴 설치 필요\n",
                    "    plt.rc('font', family='NanumBarunGothic')\n",
                    "\n",
                    "plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지\n",
                    "\n"
                ]
                
                # Extract the rest of the code (plotting part)
                # We look for where the plotting part starts. In the original code it was after sns.set_style OR around line 20 of the cell
                
                # Let's verify the split point. Original code had:
                # ...
                # plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지\n
                # sns.set_style("whitegrid") # 깔끔한 배경 스타일\n
                # \n
                # # -------------------------------------------------------\n
                # # 2. 시각화 그리기\n
                
                # We can find the index of "# 2. 시각화 그리기"
                split_index = -1
                for i, line in enumerate(source):
                    if "# 2. 시각화 그리기" in line:
                        split_index = i
                        break
                
                if split_index != -1:
                    # Keep the header comment line because we want to preserve structure, but maybe just take from that line onwards
                    # Actually, the prefix I defined above replaces everything up to that point.
                    # So we take from split_index - 1 (the separator line) or just from split_index.
                    
                    # Let's verify if there is a separator line before it.
                    # In original: 
                    # # -------------------------------------------------------\n
                    # # 2. 시각화 그리기\n
                    
                    # Search for the separator before it if possible
                    if split_index > 0 and "---" in source[split_index-1]:
                        rest_of_code = source[split_index-1:]
                    else:
                        rest_of_code = source[split_index:]
                        
                    cell['source'] = new_source_prefix + rest_of_code
                    modified = True
                    print("Cell modified.")
                else:
                    print("Could not find split point '# 2. 시각화 그리기'. Aborting modification to avoid data loss.")

    if modified:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False) # indent=1 to match usual notebook format roughly
        print(f"Successfully updated {target_file}")
    else:
        print("No changes made.")

except Exception as e:
    print(f"Error: {e}")
