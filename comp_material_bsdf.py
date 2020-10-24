# 各種ライブラリインポート
import bpy

# プリンシプルBSDFノードで比較対象とする入力端子の名前をリストで定義する
def_comp_bsdfnode_input_list = [
    "Base Color",
    "Subsurface",
    "Subsurface Radius",
    "Subsurface Color",
    "Metallic",
    "Specular",
    "Specular Tint",
    "Roughness",
    "Anisotropic",
    "Anisotropic Rotation",
    "Sheen",
    "Sheen Tint",
    "Clearcoat",
    "Clearcoat Roughness",
    "IOR",
    "Transmission",
    "Transmission Roughness",
    "Emission",
    "Alpha",
    "Normal",
    "Clearcoat Normal",
    "Tangent",
]

# 指定したオブジェクトのマテリアルを類似マテリアルにマージする
def material_marge_object(arg_object:bpy.types.Object) -> bool:
    """指定したオブジェクトのマテリアルを類似マテリアルにマージする
    以下の条件で類似マテリアルを判断する
    1.指定マテリアルのアクティブな出力ノードにノードが接続されているか
    2.アクティブな出力ノードに接続されたノードはプリンシプルBSDFか
    3.プリンシプルBSDFの比較対象の入力端子にリンクが貼られておらず、デフォルト値が有効か
    4.デフォルト値が有効な場合、その入力端子が全て一致すれば類似と判断する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bool: 実行正否
    """

    # オブジェクトがメッシュであるか確認する
    if arg_object.type != 'MESH':
        # 指定オブジェクトがメッシュでない場合は処理しない
        return None

    # オブジェクトのマテリアルスロットを走査する
    for check_material_slot in arg_object.material_slots:
        # スロットのマテリアルを取得
        check_mat = check_material_slot.material
        # 全マテリアルデータを走査する
        for comp_material_slot in arg_object.material_slots:
            # スロットのマテリアルを取得
            comp_mat = comp_material_slot.material
            # 一致マテリアルを検出する前に自身がリストに出た場合
            # マージ処理を行わない
            if check_mat.name == comp_mat.name:
                break

            # マテリアルの比較処理
            comp_result = comp_material_bsdf(check_mat, comp_mat)

            # 比較結果をチェックする
            if comp_result:
                # マテリアルを一致したものに差し替え
                check_material_slot.material = comp_mat
                # マージ処理を終了する
                break

    return True

# 指定マテリアルのBSDFノードを比較する
def comp_material_bsdf(arg_material_one:bpy.types.Material,
  arg_material_two:bpy.types.Material) -> bool:
    """指定マテリアルのBSDFノードを比較する
    受け渡したマテリアルの出力ノードに接続されたプリシプルBSDFノードを比較する
    比較対象の入力端子のデフォルト値が有効、かつ、全て同一の場合、Trueを返す

    Args:
        arg_material_one (bpy.types.Material): 比較マテリアル１
        arg_material_two (bpy.types.Material): 比較マテリアル２

    Returns:
        bool: 比較結果(一致：True)
    """

    # マテリアルの出力ノードにプリンシプルBSDFノードが接続されているかチェックする
    if check_surface_bsdf(arg_material_one) == False:
        # プリシプルBSDF出なかった場合は処理を終了して False を返す
        return False
    
    # マテリアルの出力ノードにプリンシプルBSDFノードが接続されているかチェックする
    if check_surface_bsdf(arg_material_two) == False:
        # プリシプルBSDF出なかった場合、処理を終了して False を返す
        return False

    # プリンシプルBSDFノードを取得する
    get_node_one = get_node_linkoutput(arg_material_one)

    # プリンシプルBSDFノードを取得する
    get_node_two = get_node_linkoutput(arg_material_two)

    # 比較結果フラグ(デフォルトで一致判定)
    comp_result = True

    # 比較対象とする入力端子を全てチェックする
    for bsdfnode_inputname in def_comp_bsdfnode_input_list:

        # デフォルト値が有効なソケットの情報を取得する
        nodesocket_one = get_nodesocket_enabledefault(arg_node=get_node_one, arg_inputname=bsdfnode_inputname)
        nodesocket_two = get_nodesocket_enabledefault(arg_node=get_node_two, arg_inputname=bsdfnode_inputname)

        # デフォルト値が有効なソケット情報を取得できたか確認する
        if ((nodesocket_one == None) or (nodesocket_two == None)):
            # ソケット情報を取得できなかった場合は不一致としてチェックを終了する
            comp_result = False
            break

        # ソケットのタイプが同一か確認する
        if (type(nodesocket_one) != type(nodesocket_two)):
            # 同一でない場合は不一致としてチェックを終了する
            comp_result = False
            break

        # タイプ毎の値比較の実施済みフラグ
        checked_flg = False

        # NodeSocketFloatのソケットの比較
        if isinstance(nodesocket_one, bpy.types.NodeSocketFloat):
            # 値が一致するか比較する
            if (nodesocket_one.default_value != nodesocket_two.default_value):
                # 値が一致しない場合は不一致としてチェックを終了する
                comp_result = False
                break
            else:
                # タイプ毎の値比較の実施済みフラグを設定する
                checked_flg = True

        # NodeSocketFloatFactorのソケットの比較
        if isinstance(nodesocket_one, bpy.types.NodeSocketFloatFactor):
            # 値が一致するか比較する
            if (nodesocket_one.default_value != nodesocket_two.default_value):
                # 値が一致しない場合は不一致としてチェックを終了する
                comp_result = False
                break
            else:
                # タイプ毎の値比較の実施済みフラグを設定する
                checked_flg = True

        # NodeSocketVectorのソケットの比較
        if isinstance(nodesocket_one, bpy.types.NodeSocketVector):
            # 値が一致するか比較する
            if ((nodesocket_one.default_value[0] != nodesocket_two.default_value[0]) or
                (nodesocket_one.default_value[1] != nodesocket_two.default_value[1]) or
                (nodesocket_one.default_value[2] != nodesocket_two.default_value[2])):
                # 値が一致しない場合は不一致としてチェックを終了する
                comp_result = False
                break
            else:
                # タイプ毎の値比較の実施済みフラグを設定する
                checked_flg = True

        # NodeSocketColorのソケットの比較
        if isinstance(nodesocket_one, bpy.types.NodeSocketColor):
            # 値が一致するか比較する
            if ((nodesocket_one.default_value[0] != nodesocket_two.default_value[0]) or
                (nodesocket_one.default_value[1] != nodesocket_two.default_value[1]) or
                (nodesocket_one.default_value[2] != nodesocket_two.default_value[2]) or
                (nodesocket_one.default_value[3] != nodesocket_two.default_value[3])):
                # 値が一致しない場合は不一致としてチェックを終了する
                comp_result = False
                break
            else:
                # タイプ毎の値比較の実施済みフラグを設定する
                checked_flg = True
        
        # 値比較を実施済みか確認する
        if checked_flg == False:
            # 合致するタイプがない場合はBSDFでないと判断して不一致としてチェックを終了する
            comp_result = False
            break

    return comp_result

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

# 指定ノードの指定入力端子名のソケットをデフォルト値が有効な場合に取得する
def get_nodesocket_enabledefault(arg_node:bpy.types.Node, arg_inputname:str) -> bpy.types.NodeSocketStandard:
    """指定ノードの指定入力端子名のソケットをデフォルト値が有効な場合に取得する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_inputname (str): 入力端子名

    Returns:
        bpy.types.NodeSocketStandard: ノードソケット(取得失敗時 None)
    """

    # 指定名の入力端子のソケットを取得する
    # (get関数は対象が存在しない場合 None が返る)
    get_NodeSocketStandard = arg_node.inputs.get(arg_inputname)

    # 指定名の入力端子が存在するか確認する
    if get_NodeSocketStandard == None:
        # 指定名の入力端子が存在しない場合はソケットを返さない
        return None

    # ベースカラーのリンクが接続されているか確認する
    if get_NodeSocketStandard.is_linked == True:
        # リンクが設定されていればデフォルト値は無効なためソケットを返さない
        return None
    
    return get_NodeSocketStandard