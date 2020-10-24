# bpyインポート
import bpy

# 指定マテリアルのアクティブな出力ノードに接続されたノードがプリンシプルBSDFかチェックする
def check_surface_bsdf(arg_material:bpy.types.Material) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたノードがプリンシプルBSDFかチェックする

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bool: プリンシプルBSDFが接続されているか
    """

    # マテリアルのノードを有効化する
    use_material_node(arg_material=arg_material)

    # アクティブな出力ノードに接続されたノードを取得する
    get_node = get_node_linkoutput(arg_material=arg_material)

    # ノードが取得できたか確認する
    if get_node == None:
        # サーフェスノードが存在しない場合はFalseを返す
        return False

    # ノードの種類がプリンシプルBSDFかチェックして結果を返す
    isBSDF = check_isnode_bsdf(get_node)

    return isBSDF


# アクティブな出力ノードに接続されたノードを取得する
def get_node_linkoutput(arg_material:bpy.types.Material) -> bpy.types.Node:
    """アクティブな出力ノードに接続されたノードを取得する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.Node: アクティブな出力ノードに接続されたノード
    """

    # 参照の保存用変数
    name_mapping = {}

    # ノード操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Node.html)
    # ノードリスト操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Nodes.html)
    # ノードツリー操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeTree.html)

    # ターゲットマテリアルのノード参照を取得する
    mat_nodes = arg_material.node_tree.nodes

    # 出力ノードを取得する変数
    output_node = None

    # 出力ノードの操作マニュアル
    # (https://docs.blender.org/api/current/bpy.types.ShaderNodeOutputMaterial.html)

    # 全ノードを走査する
    for check_node in mat_nodes:
        # ノードタイプを取得する
        node_idname = check_node.bl_idname

        # ノードタイプが出力ノードか確認する
        if node_idname == 'ShaderNodeOutputMaterial':
            # アクティブな出力ノードのフラグを取得する
            is_activeoutput = check_node.is_active_output

            # アクティブな出力ノードかチェックする
            if is_activeoutput == True:
                # アクティブな出力ノードなら保持する
                output_node = check_node

    # 出力ノードが取得できたか確認する
    if output_node == None:
        # 出力ノードが存在しない場合は処理しない
        return None
    
    # ノードソケット操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeSocket.html)

    # 出力ノードのサーフェス入力(1番目の入力)のリンクを確認する
    surface_input = output_node.inputs[0]

    # リンクが接続されているか確認する
    if surface_input.is_linked == False:
        # 出力ノードにサーフェスノードが接続されていない場合は処理しない
        return None

    # リンク操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeLink.html#bpy.types.NodeLink)

    # リンクの一覧を取得する
    mat_links = arg_material.node_tree.links

    # 接続元ノードを取得する変数
    surface_node = None

    # リンクを走査する
    for check_link in mat_links:
        # 接続先が出力ノードのサーフェス入力か確認する
        if check_link.to_socket == surface_input:
            # リンクの接続元ノードを取得する
            surface_node = check_link.from_node
    
    # 接続元ノードが取得できたか確認する
    if surface_node == None:
        # 接続元ノードが存在しない場合は処理しない
        return None
    
    # 接続元となっているサーフェスノードを返却する
    return_node = surface_node

    return return_node


# 対象マテリアルのノードを有効化する
def use_material_node(arg_material:bpy.types.Material):
    """対象マテリアルのノードを有効化する

    Args:
        arg_material (bpy.types.Material): 対象マテリアル
    """

    # マテリアル操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Material.html)

    # ノードが無効な場合、有効化する
    if arg_material.use_nodes == False:
        arg_material.use_nodes = True

    return


# 指定ノードがプリンシプルBSDFかチェックする
def check_isnode_bsdf(arg_node:bpy.types.Node) -> bool:
    """指定ノードがプリンシプルBSDFかチェックする

    Args:
        arg_node (bpy.types.Node): 指定ノード

    Returns:
        bool: プリンシプルBSDFか否か
    """

    # チェック結果
    isBSDF = False

    # ノードタイプを取得する
    node_idname = arg_node.bl_idname

    # ノードタイプがプリンシプルBSDFノードか確認する
    if node_idname == 'ShaderNodeBsdfPrincipled':
        # プリンシプルBSDFならTrueを返す
        isBSDF = True

    return isBSDF