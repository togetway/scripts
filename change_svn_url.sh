#!/bin/bash
#Written by jason
#Readme: �޸��Ѵ���svnĿ¼��·��


USER=`/usr/bin/whoami`

#����svn�û�������
SVN_USER='xxx'
SVN_PWD='xxx'

if [ $USER != 'root' ];then
	echo "Please use root run scripts."
	exit 1
fi


##
change_svn_url()
{
local DIR=$1    #����Ŀ¼
local NEW_URL=$2    #��Ӧsvn��url
if [ -d $DIR ];then
	URL=`svn info $DIR | grep ^URL | awk '{print $2}'`
	if [ -n "$URL" ];then
		cd $DIR && svn sw --relocate $URL $NEW_URL --username=$SVN_USER --password=$SVN_PWD
		if [ $? -eq 0 ];then
			echo "change url OK"
		else
			echo "change url Fail"
			exit 1
		fi
	else
        echo '$DIR no svn Dir'
    fi
else
	echo "No Find dir $DIR"
	exit 1
fi
}


change_svn_url '/usr/local/svn/test' 'http://localhost/svn/test'


