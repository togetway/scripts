#!/bin/bash
#Written by jason
#Readme: 修改已存在svn目录的路径


USER=`/usr/bin/whoami`

#定义svn用户名密码
SVN_USER='xxx'
SVN_PWD='xxx'

if [ $USER != 'root' ];then
	echo "Please use root run scripts."
	exit 1
fi


##
change_svn_url()
{
local DIR=$1    #绝对目录
local NEW_URL=$2    #对应svn的url
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


