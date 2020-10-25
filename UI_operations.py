# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "check_surface_bsdf" in locals():
        importlib.reload(check_surface_bsdf)
    if "comp_material_bsdf" in locals():
        importlib.reload(comp_material_bsdf)
    if "control_materialslot_utilities" in locals():
        importlib.reload(control_materialslot_utilities)
import bpy
from . import check_surface_bsdf
from . import comp_material_bsdf
from . import control_materialslot_utilities


# BSDFマテリアルマージ実行ボタンの処理を実行する
def UI_bsdf_material_marge(arg_target_object:bpy.types.Object) -> str:
    """BSDFマテリアルマージ実行ボタンの処理を実行する

    Returns:
        str: エラーメッセージ(正常時 None)
    """

    # 対象オブジェクトのマテリアルが全てプリンシプルBSDFを使用したノードかチェックする
    for check_material_slot in arg_target_object.material_slots:
        # スロットのマテリアルを取得
        check_mat = check_material_slot.material

        # マテリアルがプリンシプルBSDFを使用したノードかチェックする
        if check_surface_bsdf.check_surface_bsdf(arg_material=check_mat) == False:
            # プリンシプルBSDFを使用していないマテリアルが含まれている場合はエラーメッセージを表示する
            return "Material : " + check_mat.name + " is not BsdfPrincipled."

    # マテリアルスロットの編集を行うため、オブジェクトモードに移行する
    mode_result = control_materialslot_utilities.set_mode_object()

    # 実行結果を確認する
    if mode_result == False:
        # 実行結果がエラーの場合はエラーメッセージを表示する
        return "Execute : Mode Change failed."

    # 指定オブジェクトのマテリアルを類似マテリアルでマージする
    comp_result = comp_material_bsdf.material_marge_object(arg_object=arg_target_object)

    # 実行結果を確認する
    if comp_result == False:
        # 実行結果がエラーの場合はエラーメッセージを表示する
        return "Execute : Merge failed."

    # 指定オブジェクトのマテリアルスロットをソートする
    sort_result = control_materialslot_utilities.sort_materialslot_name(arg_object=arg_target_object)
    
    # 実行結果を確認する
    if sort_result == False:
        # 実行結果がエラーの場合はエラーメッセージを表示する
        return "Execute : Sort failed."

    # 指定オブジェクトのマテリアルスロットをソートする
    delete_result = control_materialslot_utilities.delate_materialslot_duplicate(arg_object=arg_target_object)
    
    # 実行結果を確認する
    if delete_result == False:
        # 実行結果がエラーの場合はエラーメッセージを表示する
        return "Execute : Delete failed."

    # 正常終了時は None を返す
    return None


