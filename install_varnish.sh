#! /bin/bash

curl -s -L https://packagecloud.io/varnishcache/varnish60lts/gpgkey | apt-key add -

. /etc/os-release

tee /etc/apt/sources.list.d/varnishcache_varnish60lts.list > /dev/null <<-EOF
deb https://packagecloud.io/varnishcache/varnish60lts/$ID/ $VERSION_CODENAME main
EOF

tee /etc/apt/preferences.d/varnishcache > /dev/null <<-EOF
Package: varnish varnish-*
Pin: release o=packagecloud.io/varnishcache/*
Pin-Priority: 1000
EOF

apt-get update

apt-get install varnish -y