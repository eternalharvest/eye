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

## BACnet による値の取得
### 同一ネットワーク内の BACnet デバイスを検索する
  BACnet では、IP アドレスの代わりに デバイスID と呼ばれる識別子を利用することで、
BACnet デバイス同士の通信が行われます。そのためBACnet の 通信を行うためには、
まず BACnet デバイスを検索する必要があります。

## BACnet シミュレータの利用
### 新規オブジェクトの登録
  BACnet Object を シミュレータに登録するには以下のコマンドを実行します。

```bash
$ eye add simulation bacnet object [NAME] [OBJECT_ID] [INSTANCE_ID]
```

  BACnet オブジェクトが登録されているかを確認するためには、bacepics 等のコマンドを
使用してください。

### 新規プロパティを登録
  作成したオブジェクトにプロパティを設定し、外部のデバイスから値を取得することが可能な
状態にします。

```bash
$ eye add simulation bacnet property [NAME] [PROPERTY_ID]
```

## BACnet プロキシ の 利用


