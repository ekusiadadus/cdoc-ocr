import re
import pandas as pd
import matplotlib.pyplot as plt

import camelot

# 2ページ目から最終頁まで、セパレーター優先、改行除去
tables = camelot.read_pdf('output.pdf', pages='1',
                          split_text=True, strip_text='\n')

dfs = []

# # dataframeに変換、ヘッダー部削除、ヘッダー追加
for table in tables:
    df = table.df
    # df.drop(0, inplace=True)
    # df.columns = ['企業・事業場名称', '所在地', '公表日', '違反法条', '事案概要', 'その他参考事項']
    dfs.append(df)

# # ページ結合
# df_black = pd.concat(dfs)

# # カンマを追加


# def ihan_conv(temp):
#     result = re.sub('条(の\d{1,3})?', lambda m: m.group(
#         0) + ', ', temp).rstrip(', ')
#     return result


# def sonota_conv(temp):
#     result = re.sub('H\d{1,2}\.\d{1,2}\.\d{1,2}',
#                     lambda m: ', ' + m.group(0), temp).lstrip(', ')
#     return result


# df_black['違反法条'] = df_black['違反法条'].apply(ihan_conv)
# df_black['その他参考事項'] = df_black['その他参考事項'].apply(sonota_conv)

# CSVファイルへ出力
# df_black.to_csv('black.csv')
df.to_csv('output.csv')

# TSVファイルへ出力
df.to_csv('output.tsv', sep='\t')

# EXCELファイルへ出力
# with pd.ExcelWriter('black.xlsx') as writer:
#     df_black.to_excel(writer, sheet_name='sheet1')
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1')
