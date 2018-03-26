# BACnet Protocol
## BACnet サービスの管理
### サービスを起動する
　BACnet サービスを利用するためには、まず BACnet サービスへの設定を実行する必要があります。
BACnet サービスは以下のコマンドを使用することで利用することが可能となります。

```bash
$ eye start bacnetd [INTERFACE] [DEVICE_ID]
```

  実際に使用する際には以下のように、インタフェース名を指定する必要があります。
BACnet の デバイス ID は省略することが可能です。（同じネットワークに同じBACnet Device ID
のBACnet デバイスが存在する際には変更を行う必要があります。）

```bash
$ eye start bacnetd eth0 1234
```

### サービスを停止する
  BACnet サービスを停止する際には、以下のコマンドを実行します。
停止する場合には、BACnet を 使用した通信を行うことが出来なくなることに注意してください。

```bash
$ eye stop bacnetd
```

## BACnet シミュレータの利用


