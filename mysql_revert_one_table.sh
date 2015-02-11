#!/bin/bash
#Written by jason
#Readme:脚本用于从数据库备份文件中，提取一个表的数据
#因为有时候我们备份的是整个数据库，而还原只要还原一个表就足够了。
usage(){
    echo " -h show this page"
    echo " -t table name"
    echo " -i database backup file"
    echo " -o the result of table sql segment"
}

while getopts t:i:o:h myarg
do
    case $myarg in
    h)
        usage
        exit 1;;
    t)
        tbname=$OPTARG;;
    i)
        infile=$OPTARG;;
    o)
        outfile=$OPTARG;;
    *)
        usage
        exit 1;;
    esac
done

check_option(){
    if [ -z "$tbname" -o -z "$infile" -o -z "$outfile" ];then
        usage
        exit 1
    fi
}

check_option

awk '/DROP TABLE IF EXISTS `'$tbname'`;/{print;while(getline line){if(line ~ /DROP TABLE IF EXISTS/){break};print line}}' $infile > $outfile

exit 0