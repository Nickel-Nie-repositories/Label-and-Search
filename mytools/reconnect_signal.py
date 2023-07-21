

def reconnect(signal, newHandler=None, oldHandler=None):
    """
    一个安全替换信号绑定的方法。
    :param signal: 信号，例如 button.clicked, shortcut.activated 等。
    :param newHandler:新的处理函数，可以不指定，那样就只是移除原先的处理函数。
    :param oldHandler:原先的处理函数，指定函数签名定向移除，可以不指定，移除所有。
    :return:
    """

    while True:
        try:
            if oldHandler is not None:
                signal.disconnect(oldHandler)
            else:
                # print("解绑 ：", signal)
                signal.disconnect()
        except RuntimeError:
            # print("解绑结束")
            break
    if newHandler is not None:
        # print("绑定：", signal, newHandler)
        signal.connect(newHandler)
