
# Настройка Hadoop кластера

## 1. Подключение к кластеру
Подключитесь к кластеру с помощью SSH:

```bash
ssh team@176.109.91.16
```

## 2. Создание связи между нодами

### 2.1 Создание пользователя hadoop и генерация SSH ключа
Для каждой ноды создайте нового пользователя hadoop:

```bash
sudo adduser hadoop
sudo -i -u hadoop
```

Сгенерируйте SSH ключ для пользователя:

```bash
ssh-keygen
cat .ssh/id_ed25519.pub
```

### 2.2 Настройка host-файлов
Отредактируйте файл `/etc/hosts` на каждой ноде:

```bash
sudo nano /etc/hosts
```

Добавьте следующие строки:

```
192.168.1.58 team-14-jn
192.168.1.59 team-14-nn 
192.168.1.60 team-14-dn-0 
192.168.1.61 team-14-dn-1
```

### 2.3 Перенос ключей и настройка SSH
Сгенерируйте SSH ключи для каждой ноды и скопируйте их на все машины:

```bash
vim ~/.ssh/authorized_keys
scp ~/.ssh/authorized_keys team-14-nn:/home/hadoop/.ssh/
scp ~/.ssh/authorized_keys team-14-dn-0:/home/hadoop/.ssh/
scp ~/.ssh/authorized_keys team-14-dn-1:/home/hadoop/.ssh/
```

Настройте SSH для работы без пароля:

```bash
sudo nano /etc/ssh/ssh_config
# Убедитесь, что параметр PasswordAuthentication установлен в no.
```

### 2.4 Установка Hadoop
Скачайте дистрибутив Hadoop:

```bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz
scp hadoop-3.4.0.tar.gz team-14-nn:/home/hadoop/hadoop-3.4.0.tar.gz
scp hadoop-3.4.0.tar.gz team-14-dn-0:/home/hadoop/hadoop-3.4.0.tar.gz
scp hadoop-3.4.0.tar.gz team-14-dn-1:/home/hadoop/hadoop-3.4.0.tar.gz
```

Распакуйте архив на всех нодах:

```bash
tar -xvzf hadoop-3.4.0.tar.gz
```

## 3. Настройка кластера

### 3.1 Проверка и настройка Java
Проверьте версию Java и добавьте путь до нее в переменные окружения:

```bash
java -version
which java
nano $HADOOP_HOME/etc/hadoop/core-site.xml
```

Добавьте следующие переменные в файл профиля:

```bash
export HADOOP_HOME=/home/hadoop/hadoop-3.4.0
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

Скопируйте профиль на все ноды:

```bash
scp ~/.profile team-14-dn-0:/home/hadoop
scp ~/.profile team-14-dn-1:/home/hadoop
```

### 3.2 Настройка Hadoop
Добавьте путь до Java в файл `hadoop-env.sh` и скопируйте его на все ноды:

```bash
vim hadoop-env.sh
scp hadoop-env.sh team-14-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/
scp hadoop-env.sh team-14-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/
```

Настройте базовый адрес и порт в файле `core-site.xml`:

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://team-14-nn:9000</value>
  </property>
</configuration>
```

Скопируйте его на все ноды:

```bash
scp core-site.xml team-14-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/
scp core-site.xml team-14-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/
```

Добавьте фактор репликации в `hdfs-site.xml`:

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
</configuration>
```

Скопируйте файл на все ноды:

```bash
scp hdfs-site.xml team-14-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/
scp hdfs-site.xml team-14-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/
```

Добавьте названия нод в файл `workers`:

```bash
team-14-nn
team-14-dn-0
team-14-dn-1
scp workers team-14-dn-0:/home/hadoop/hadoop-3.4.0/etc/hadoop/
scp workers team-14-dn-1:/home/hadoop/hadoop-3.4.0/etc/hadoop/
```

## 4. Запуск кластера

### 4.1 Форматирование файловой системы и запуск HDFS
Перейдите в директорию Hadoop и выполните команды:

```bash
bin/hdfs namenode -format
sbin/start-dfs.sh
```

## 5. Настройка веб-интерфейса

### 5.1 Настройка реверс-прокси на Nginx
Создайте файл конфигурации для неймноды:

```bash
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/nn
sudo vim /etc/nginx/sites-available/nn
```

Отредактируйте следующие строки:

```
listen 9870 default_server;
proxy_pass http://team-14-nn:9870;
```

Создайте символическую ссылку на новый файл конфигурации и перезапустите Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/nn /etc/nginx/sites-enabled/nn
sudo systemctl reload nginx
```
