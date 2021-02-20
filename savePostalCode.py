# -*- coding: utf-8 -*-
import csv
import pathlib
import psycopg2

try:
    connection = psycopg2.connect("host=localhost port=5432 dbname=testdb user=YasuoKatou")
    #print(str(connection.get_backend_pid()))
    if connection.autocommit:
        connection.autocommit = False
        print('自動コミットをオフに設定しました.')
    else:
        print('トランザクションを開始しています.')
    cur = connection.cursor()

    prevCode7 = ''
    prevCity  = ''
    ins_num   = 0
    upd_num   = 0
    csvPath = pathlib.Path('Z:\workspace\ZipNo\ken_all\KEN_ALL.CSV')
    with csvPath.open(mode='r', encoding='shift_jis') as f:
        reader = csv.reader(f, delimiter=',' )
        for row in reader:
            #print(row)
            if prevCity  != row[6]:
                #処理する都道府県名が変わったとき
                prevCity = row[6]
                print(prevCity + 'を処理します.')
            if prevCode7 == row[2]:
                #前の行と同じ郵便番号
                cur.execute("update postal_code set" \
                    "  area3_kana = area3_kana || %s" \
                    ", area3      = area3      || %s" \
                    " where code_7 = %s", (row[5], row[8], prevCode7))
                upd_num += 1
            else:
                #前の行と異なる郵便番号
                prevCode7 = row[2]
                cur.execute("insert into postal_code" \
                    " (jis_x0401_x0402, code_5, code_7" \
                    ", area1_kana, area2_kana, area3_kana" \
                    ", area1, area2, area3, flag1, flag2, flag3, flag4" \
                    ", update_delete_code, update_reason_code) values" \
                    " (%s, %s, %s, %s, %s, %s, %s, %s, %s" \
                    ", %s, %s, %s, %s, %s, %s)", row)
                ins_num += 1
            #print('ins:%d, upd:%d' % (ins_num, upd_num))
    connection.commit()
    print('正常終了しました.(追加:%d, 更新:%d)' % (ins_num, upd_num))
finally:
    cur.close()
    connection.close()
#[EOF]