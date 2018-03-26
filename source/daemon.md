# Daemon Manager
## 自動起動の設定
  ここでは、EYED を 自動起動サービスとして登録する方法について説明します。
デーモンの管理は、supervisor を使用します。

### supervisor の インストール
```bash
sudo apt-get install supervisor
```

### サービスの登録
```bash
supervisorctl add eyed
```

### サービスの起動
```bash
supervisorctl start eyed
```

