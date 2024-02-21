# ELK-Centos8
Install ELK Stack(Elastic Search, Kibana and Logstash) use SSL Lets Encrypt, full screenshot about ELK go to website.

## Documentation technical Fanintek : CentOS 8 -> 4 CPU 8gb Ram
1. Install ELK Stack: Elastic Search, Kibana, Logstash
2. Cek status koneksi cluster
3. Cek Fungsi ELK
4. Cek pemahaman dan fundamental
5. Scripting Python : Buat script untuk bisa membuat log dari status port apa saja yang sedang aktif dan menulisnya dalam format .log
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Setup Centos 8
1. timedatectl set-timezone 'Asia/Jakarta'
2. sudo yum -y install epel-release
3. sudo yum -y install htop
4. sudo yum -y update
5. sudo reboot

## Java JDK 11
1. sudo yum -y install java-11-openjdk java-11-openjdk-devel
2. java -version

## Elastic 8.12.1
Import GPG key
1. sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
2. vi /etc/yum.repos.d/elasticsearch.repo
3. [elasticsearch-8.x]
name=Elasticsearch repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
4. sudo yum clean all
   sudo yum makecache
5. sudo yum install elasticsearch
6. sudo vi /etc/elasticsearch/elasticsearch.yml -> file tertera di elasticsearch.yml tidak termasuk token password
7. sudo systemctl start elasticsearch
8. sudo systemctl enable elasticsearch
9. sudo systemctl status elasticsearch
10. curl -v -u elastic https://elk.adamrizqi.my.id:9200

{
  "name" : "elk.adamrizqi.my.id",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "2vJbugVMSFqwPFebs5OeGg",
  "version" : {
    "number" : "8.12.1",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "6185ba65d27469afabc9bc951cded6c17c21e3f3",
    "build_date" : "2024-02-01T13:07:13.727175297Z",
    "build_snapshot" : false,
    "lucene_version" : "9.9.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}

## Logstash install & configure
1. sudo yum -y install logstash
2. sudo vi /etc/logstash/conf.d/ -> if you use SSL don't forget to set conf username elasticsearch / example: -elastic pass:..... see file up there.
3. sudo systemctl start logstash
4. sudo systemctl enable logstash
5. sudo journalctl -u logstash -f / sudo tail -n 100 /var/log/logstash/logstash-plain.log
6. sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
### Have 2 file conf logstash
1. logstash-its.conf -> check beat port udp and beat no need set
2. port_status.conf -> check port log status from index port_status elasticsearch -> need run scripting python pyportelastic.py 

## Kibana Install & Configuration
1. sudo yum -y install kibana
2. sudo vi /etc/kibana/kibana.yml -> file tertera di kibana.yml tidak termasuk token password
3. sudo systemctl enable --now kibana
4. sudo systemctl start kibana

## Firewall
1. sudo yum -y install firewalld
2. sudo systemctl start firewalld
3. sudo systemctl enable firewalld
4. sudo firewall-cmd --state 
5. sudo firewall-cmd --add-port=5601/tcp --permanent
6. sudo firewall-cmd --add-port=5044/tcp --permanent
7. Tambah firewal sesuai kebutuhan. port 9200, 9300, 80
8. firewall-cmd --list-ports
9. sudo firewall-cmd --reload

## DNS Cloudflare
1. Set DNS subdomain -> elk.adamrizqi.my.id & kibana.adamrizqi.my.id 
2. Set auto HTTPS - False 

## SSL Let's Encrypt
1. https://certbot.eff.org/ -> See installation
2. sudo yum -y install snapd
3. https://snapcraft.io/docs/installing-snap-on-centos -> For centos -> sudo systemctl enable --now snapd.socket -> sudo ln -s /var/lib/snapd/snap /snap
4. sudo snap install --classic certbot
5. sudo ln -s /snap/bin/certbot /usr/bin/certbot
6. sudo certbot certonly --standalone
7. elk.adamrizqi.my.id , kibana.adamrizqi.my.id
8. File sudah jadi akan ada di /etc/letsencrypt/archive -> copy elk.adamrizqi.my.id & kibana.adamrizqi.my.id kedalam -> /etc/kibana/certs & /etc/elasticsearch/certs
   atau bisa cek file diatas.

## Configuration Security Password
1. cd /usr/share/elasticsearch/bin
2. ./elasticsearch-service-tokens create elastic/kibana kibana_token -> AAEAAWVsYXN0aWMva2liYW5hL2tpYmFuYV90b2tlbjpRVkhQOF9zWVFjYXItYVYyVkR2X3h3
3. vi token -> save token
4. ./usr/share/kibana/bin/kibana-verification-code -> enter token : AAEAAWVsYXN0aWMva2liYW5hL2tpYmFuYV90b2tlbjpRVkhQOF9zWVFjYXItYVYyVkR2X3h3
5. cd /etc/kibana/ -> token alredy installed kibana.keystore

### Scripting python pyportlog.py -> Get Active Port , send to file .log without elasticsearch
1. sudo yum -y install net-tools
2. sudo yum -y python3
3. chmod +x pyportlog.py
4. python3 pyportlog.py

### Scripting python pyportelastic.py -> Get Active Port , send to file .log and send to elasticsearch index management / index pattern
1. sudo yum -y install python3-pip
2. pip3 install psutil elasticsearch
3. chmod +x pyportelastic.py
4. python3 pyportelastic.py

### Notes: Install psutil error? run this step
1. sudo -H pip3 install --upgrade pip
2. sudo yum groupinstall "Development Tools"
3. sudo yum install gcc python3-devel
4. pip3 install psutil

### Notes: Install elasticsearch error? run this step
1. pip3 install --upgrade requests
2. pip3 install --upgrade elasticsearch
- Still get error how to fix?
4. Install virtualenv -> sudo -H pip3 install virtualenv
5. Create a virtual environment -> python3 -m venv myenv
6. pip3 install elasticsearch
7. Finish, dont forget for leave virtualenv -> deactivate
  
# Activate the virtual environment
source myenv/bin/activate

----------
## If have problem SSL and Token
1. chown -R yourusername:yourusername / example: chown -R kibana:kibana ./ -> for all folder

----------
## Tidak terpakai
## SSL Self Signed
- cd /usr/share/elasticsearch/bin
1. #### Elastic SSL Self Signed

- ./elasticsearch-certutil ca --pem --out /etc/elasticsearch/certs/ca.zip

- ./elasticsearch-certutil cert --out /etc/elasticsearch/elastic.zip --name elastic --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key --dns elk.adamrizqi.my.id --pem

2. #### Kibana SSL Self Signed

- ./elasticsearch-certutil cert --out /root/kibana/kibana.zip --name kibana --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key --dns kibana.adamrizqi.my.id --pem

