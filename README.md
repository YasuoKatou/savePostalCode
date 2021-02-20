## 郵便番号データ初期登録  
データは、[読み仮名データの促音・拗音を小書きで表記しないもの(zip形式)](https://www.post.japanpost.jp/zipcode/dl/oogaki-zip.html)から「全国一括」(CSV形式)を[ダウンロード](https://www.post.japanpost.jp/zipcode/dl/oogaki/zip/ken_all.zip)してPostgreSQLのDBに登録する
### 対象DB  
* PostgreSQL 12

### 利用方法
* データベースの接続先を環境に合わせて変更（７行目）
* CSVパスを環境に合わせて変更（２０行目）

### テーブル構造  
今回プライマリーキーの設定は、行っていません。理由は、７桁の郵便番号がユニークにならないためです。（下記*4より）  

    -- drop table if exists postal_code;
    create table if not exists postal_code (
       jis_x0401_x0402    char(   5) NOT NULL       --全国地方公共団体コード
     , code_5          varchar(   5) NOT NULL       --（旧）郵便番号（5桁）
     , code_7          varchar(   7) NOT NULL       --郵便番号（7桁）
     , area1_kana      varchar(  20) NOT NULL       --都道府県名ｶﾅ
     , area2_kana      varchar( 128) NOT NULL       --市区町村名ｶﾅ
     , area3_kana      varchar(1024) NOT NULL       --町域名ｶﾅ
     , area1           varchar(  20) NOT NULL       --都道府県名
     , area2           varchar( 128) NOT NULL       --市区町村名
     , area3           varchar(1024) NOT NULL       --町域名
     , flag1              char(   1) NOT NULL       --(*1)一町域が二以上の郵便番号で表される
     , flag2              char(   1) NOT NULL       --(*2)小字毎に番地が起番されている町域
     , flag3              char(   1) NOT NULL       --(*3)丁目を有する町域
     , flag4              char(   1) NOT NULL       --(*4)一つの郵便番号で二以上の町域を表す
     , update_delete_code char(   1) NOT NULL       --(*5)更新の表示
     , update_reason_code char(   1) NOT NULL       --(*6)変更理由
    );
    
    COMMENT ON TABLE postal_code IS '郵便番号';
    COMMENT ON COLUMN postal_code.jis_x0401_x0402 IS '全国地方公共団体コード';
    COMMENT ON COLUMN postal_code.code_5          IS '（旧）郵便番号（5桁）';
    COMMENT ON COLUMN postal_code.code_7          IS '郵便番号（7桁）';
    COMMENT ON COLUMN postal_code.area1_kana      IS '都道府県名ｶﾅ';
    COMMENT ON COLUMN postal_code.area2_kana      IS '市区町村名ｶﾅ';
    COMMENT ON COLUMN postal_code.area3_kana      IS '町域名ｶﾅ';
    COMMENT ON COLUMN postal_code.area1           IS '都道府県名';
    COMMENT ON COLUMN postal_code.area2           IS '市区町村名';
    COMMENT ON COLUMN postal_code.area3           IS '町域名';
    COMMENT ON COLUMN postal_code.flag1           IS '一町域で複数の郵便番号';   -- *1
    COMMENT ON COLUMN postal_code.flag2           IS '小字毎に番地が起番';       -- *2
    COMMENT ON COLUMN postal_code.flag3           IS '丁目を有する町域';         -- *3
    COMMENT ON COLUMN postal_code.flag4           IS '一郵便番号の複数の町域';   -- *4
    COMMENT ON COLUMN postal_code.update_delete_code IS '更新の表示';            -- *5
    COMMENT ON COLUMN postal_code.update_reason_code IS '変更理由';              -- *6
    
    /*
    (*1) 「1」該当、「0」該当せず
    (*2) 「1」該当、「0」該当せず
    (*3) 「1」該当、「0」該当せず
    (*4) 「1」該当、「0」該当せず
    (*5) 更新の表示
         「0」変更なし
         「1」変更あり  （「変更あり」とは追加および修正により更新されたデータを示すもの）
         「2」廃止（廃止データのみ使用）
    (*6) 変更理由
         「0」変更なし
         「1」市政・区政・町政・分区・政令指定都市施行
         「2」住居表示の実施
         「3」区画整理
         「4」郵便区調整等
         「5」訂正
         「6」廃止（廃止データのみ使用）
    */
