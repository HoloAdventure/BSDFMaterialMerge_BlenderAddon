# bpyインポート
import bpy

# オブジェクトモードへの移行
# モード切替のマニュアル
# (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
def set_mode_object() -> bool:
    """オブジェクトモードへの移行

    Returns:
        bool -- 実行の正否
    """

    # オブジェクトモードに移行する
    # モード切替のマニュアル
    # (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
    # 切り替え可能なモードの種類
    #   OBJECT：オブジェクトモード
    #   EDIT：編集モード
    #   POSE：ポーズモード
    #   SCULPT：スカルプトモード
    #   VERTEX_PAINT：頂点ペイントモード
    #   WEIGHT_PAINT：ウェイトペイントモード
    #   TEXTURE_PAINT：テクスチャペイントモード
    #   PARTICLE_EDIT：パーティクル編集モード
    #   EDIT_GPENCIL：グリースペンシル編集モード
    #   SCULPT_GPENCIL：グリースペンシルスカルプトモード
    #   PAINT_GPENCIL：グリースペンシルペイントモード
    #   WEIGHT_GPENCIL：グリースペンシルウェイトモード
    # toggle:Trueの場合、既に編集モードの時、オブジェクトモードに戻る
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    return True

# 指定オブジェクトのマテリアルスロットをソートする
def sort_materialslot_name(arg_object:bpy.types.Object) -> bool:
    """指定オブジェクトのマテリアルスロットをソートする

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bool: 実行正否
    """

    # オブジェクトがメッシュであるか確認する
    if arg_object.type != 'MESH':
        # 指定オブジェクトがメッシュでない場合は処理しない
        return None

    # 比較継続フラグ
    change_flg = True

    # 並び替えが完了するまでループ
    while change_flg:
        # 比較継続フラグを初期化する
        change_flg = False

        # マテリアルスロットを走査する
        for num in range(len(arg_object.material_slots)-1):
            # マテリアルを取得する
            check_mat = arg_object.material_slots[num].material
            comp_mat = arg_object.material_slots[num+1].material

            # マテリアル名を比較する
            if check_mat.name > comp_mat.name:
                # 位置を入れ替える
                arg_object.active_material_index = num
                bpy.ops.object.material_slot_move(direction='DOWN')

                # 比較を継続する
                change_flg = True

    return True

# マテリアルスロットの隣り合った重複を削除する
def delate_materialslot_duplicate(arg_object:bpy.types.Object) -> bool:
    """指定オブジェクトのマテリアルスロットをソートする

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bool: 実行正否
    """

    # オブジェクトがメッシュであるか確認する
    if arg_object.type != 'MESH':
        # 指定オブジェクトがメッシュでない場合は処理しない
        return None

    # 重複しているマテリアルスロットを削除する
    # 削除処理を行うので逆順に要素を追う
    for num in range(len(arg_object.material_slots)-1)[::-1]:
        # マテリアルを取得する
        check_mat = arg_object.material_slots[num].material
        comp_mat = arg_object.material_slots[num+1].material

        # マテリアル名を比較する
        if check_mat.name == comp_mat.name:
            # マテリアル名が同じならば削除する
            arg_object.active_material_index = num + 1
            bpy.ops.object.material_slot_remove()

    return True