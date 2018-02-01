# EYE
 EYE is a developped for monitoring agent for distributed enviroment

# Supported Protocol
- ICMP
- BACnet

# Install EYED
## Dependency
  EYED uses the supervisor for manage the daemon.
It needs a install from apt package manager.

```bash
sudo apt-get install supervisor
```

# BACnet
  You can easily install the EYE by pip command.
```python
pip install git+https://github.com/ThousandMileEye/eye.git
```

  After execute pip, you can launch EYED API Server by eyed commad.
```python
eyed
```

## Manage eyed as a service
  If you would like to use eyed as a service, You can use supervisor daemon.
Supervisor is a quite useful tool for mange python services as a daemon.
You can install supervisord by apt or yum command.

### Install supervisor manage eyed as a service
```
apt-get install supervisor
```

### Start eyed service
```
supervisorctl add eyed
supervisorctl start eyed
```

