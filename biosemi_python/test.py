from connectBiosemi import ActiveTwo

if __name__ == '__main__':

    # 初始化
    device = ActiveTwo(host='127.0.0.1', sfreq=512, port=778, nchannels=32, tcpsamples=4)

    # 读取30s的数据，并打印出来
    for run in range(30):
        rawdata = device.read(duration=1.0)
        print rawdata