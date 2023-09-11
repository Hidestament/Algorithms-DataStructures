def z_algorithm(S: str) -> list[int]:
    """文字列Sの各iについて、SとS[i:]の最長共通接頭辞の長さを求める

    Args:
        S (str): 文字列

    Returns:
        list[int]: 各iについて、SとS[i:]の最長共通接頭辞の長さ

    TimeComplexity:
        O(len(S))
    """
    if len(S) == 1:
        return [1]

    N = len(S)
    z = [0] * N

    # 既に調べた最長区間 [last_l, last_r]
    last_l, last_r = -1, -1
    for i in range(1, N):
        # これまで計算した結果が使用できない場合
        if last_r < i:
            j = 0
        else:
            k = i - last_l
            j = min(z[k], last_r - last_l + 1 - k)

        while (i + j < N) and (S[i + j] == S[j]):
            j += 1

        z[i] = j
        if last_r <= i + j - 1:
            last_l, last_r = i, i + j - 1

    z[0] = N
    return z
