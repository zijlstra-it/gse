#!/bin/bash

read_authtoken() {
	cat gse.conf | grep "^authtoken " | sed 's/^authtoken //g'
}

show_usage() {
	echo "usage: gse.sh <hostname> <path> <redirect-url>"	
}

if [ "$#" -ne 3 ]; then
	show_usage
else
	authtoken=$(read_authtoken)
	success=$(curl -s -X POST -H GSE_path:$2 -H GSE_url:$3 -H GSE_authtoken:$authtoken http://$1$2 | grep '<title>Redirecting...</title>')	
	if [ -z "$success" ]; then
		echo "Error adding redirect (3)"
	else
		echo "Redirect added"
	fi
fi
