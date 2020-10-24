# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "UI_operations" in locals():
        importlib.reload(UI_operations)
import bpy
from . import UI_operations

# bl_infoでプラグインに関する情報の定義を行う
bl_info = {
    "name": "HoloMon BSDF Material Marge Addon",     # プラグイン名
    "author": "HoloMon",                             # 制作者名
    "version": (0, 99),                               # バージョン
    "blender": (2, 80, 0),                           # 動作可能なBlenderバージョン
    "support": "TESTING",                            # サポートレベル
    "category": "Properties",                        # カテゴリ名
    "location": "View3D > Sidebar > BSDFMarge",      # ロケーション
    "description": "Addon BSDF Material Marge",      # 説明文
    "location": "",                                  # 機能の位置付け
    "warning": "",                                   # 注意点やバグ情報
    "doc_url": "",                                   # ドキュメントURL
}

# 利用するタイプやメソッドのインポート
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty

# 継承するクラスの命名規則は以下の通り
# [A-Z][A-Z0-9_]*_(継承クラスごとの識別子)_[A-Za-z0-9_]+
# クラスごとの識別子は以下の通り
#   bpy.types.Operator  OT
#   bpy.types.Panel     PT
#   bpy.types.Header    HT
#   bpy.types.MENU      MT
#   bpy.types.UIList    UL

# マテリアルベイクの実行パネル(3Dビュー)
class HOLOMON_PT_addon_bsdf_material_marge(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "BSDF Material Marge"
    # クラスのIDを定義する
    # 命名規則は CATEGORY_PT_name
    bl_idname = "HOLOMON_PT_addon_bsdf_material_marge"
    # パネルを使用する領域を定義する
    # 利用可能な識別子は以下の通り
    #   EMPTY：無し
    #   VIEW_3D：3Dビューポート
    #   IMAGE_EDITOR：UV/画像エディター
    #   NODE_EDITOR：ノードエディター
    #   SEQUENCE_EDITOR：ビデオシーケンサー
    #   CLIP_EDITOR：ムービークリップエディター
    #   DOPESHEET_EDITOR：ドープシート
    #   GRAPH_EDITOR：グラフエディター
    #   NLA_EDITOR：非線形アニメーション
    #   TEXT_EDITOR：テキストエディター
    #   CONSOLE：Pythonコンソール
    #   INFO：情報、操作のログ、警告、エラーメッセージ
    #   TOPBAR：トップバー
    #   STATUSBAR：ステータスバー
    #   OUTLINER：アウトライナ
    #   PROPERTIES：プロパティ
    #   FILE_BROWSER：ファイルブラウザ
    #   PREFERENCES：設定
    bl_space_type = 'VIEW_3D'
    # パネルが使用される領域を定義する
    # 利用可能な識別子は以下の通り
    # ['WINDOW'、 'HEADER'、 'CHANNELS'、 'TEMPORARY'、 'UI'、
    #  'TOOLS'、 'TOOL_PROPS'、 'PREVIEW'、 'HUD'、 'NAVIGATION_BAR'、
    #  'EXECUTE'、 'FOOTER'の列挙型、 'TOOL_HEADER']
    bl_region_type = 'UI'
    # パネルタイプのオプションを定義する
    # DEFAULT_CLOSED：作成時にパネルを開くか折りたたむ必要があるかを定義する。
    # HIDE_HEADER：ヘッダーを非表示するかを定義する。Falseに設定するとパネルにはヘッダーが表示される。
    # デフォルトは {'DEFAULT_CLOSED'}
    bl_options = {'DEFAULT_CLOSED'}
    # パネルの表示順番を定義する
    # 小さい番号のパネルは、大きい番号のパネルの前にデフォルトで順序付けられる
    # デフォルトは 0
    bl_order = 0
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "MRTK"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout

        # 要素行を作成する
        objectslect_row = draw_layout.row()
        # オブジェクト選択用のカスタムプロパティを配置する
        objectslect_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_objectselect", text="Target")

        # 要素行を作成する
        button_row = draw_layout.row()
        # ベイクを実行するボタンを配置する
        button_row.operator("holomon.bsdf_material_marge")

# マテリアルベイクの実行オペレーター
class HOLOMON_OT_addon_bsdf_material_marge(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = "holomon.bsdf_material_marge"
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "BSDF Marge"
    # クラスの説明文
    # (マウスオーバー時に表示)
    dl_description = "BSDF Material Marge Addon"
    # クラスの属性
    # 以下の属性を設定できる
    #   REGISTER      : Operatorを情報ウィンドウに表示し、やり直しツールバーパネルをサポートする
    #   UNDO          : 元に戻すイベントをプッシュする（Operatorのやり直しに必要）
    #   UNDO_GROUPED  : Operatorの繰り返しインスタンスに対して単一の取り消しイベントをプッシュする
    #   BLOCKING      : 他の操作がマウスポインタ―を使用できないようにブロックする
    #   MACRO         : Operatorがマクロであるかどうかを確認するために使用する
    #   GRAB_CURSOR   : 継続的な操作が有効な場合にオペレーターがマウスポインターの動きを参照して、操作を有効にする
    #   GRAB_CURSOR_X : マウスポインターのX軸の動きのみを参照する
    #   GRAB_CURSOR_Y : マウスポインターのY軸の動きのみを参照する
    #   PRESET        : Operator設定を含むプリセットボタンを表示する
    #   INTERNAL      : 検索結果からOperatorを削除する
    # 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.bl_options
    bl_options = {'REGISTER', 'UNDO'}

    # Operator実行時の処理
    def execute(self, context):
        # カスタムプロパティから指定中のオブジェクトを取得する
        target_object = context.scene.holomon_mrtk_channelmap_maker.prop_objectselect

        # 指定中のオブジェクトを確認する
        if target_object == None:
            # オブジェクトが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : target object.")
            return {'CANCELLED'}

        # チャネルマップ作成を実行する
        error_message = UI_operations.UI_bsdf_material_marge(arg_target_object=target_object)
        
        # エラーメッセージの有無を確認する
        if error_message != None:
            # エラーメッセージが設定されている場合はエラーメッセージを表示する
            self.report({'ERROR'}, error_message)
            return {'CANCELLED'}

        return {'FINISHED'}


# マテリアルベイクパネルのプロパティ
class HOLOMON_addon_bsdf_material_marge_properties(PropertyGroup):
    # オブジェクト選択時のチェック関数を定義する
    def prop_object_select_poll(self, context, ):
        # メッシュオブジェクトのみ選択可能
        if(context and context.type in ('MESH', )):
            return True
        return False

    # シーン上のパネルに表示するオブジェクト選択用のカスタムプロパティを定義する
    prop_objectselect: PointerProperty(
        name = "Select Object",         # プロパティ名
        type = bpy.types.Object,        # タイプ
        description = "",               # 説明文
        poll = prop_object_select_poll, # チェック関数
    )


# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_addon_bsdf_material_marge,
    HOLOMON_OT_addon_bsdf_material_marge,
    HOLOMON_addon_bsdf_material_marge_properties,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_bsdf_material_marge = PointerProperty(type=HOLOMON_addon_bsdf_material_marge_properties)

# 作成クラスと定義の登録解除メソッド
def unregister():
    # シーン情報のカスタムプロパティを削除する
    del bpy.types.Scene.holomon_bsdf_material_marge
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)



# 実行時の処理
if __name__ == "__main__":
    # 作成クラスと定義を登録する
    register()


