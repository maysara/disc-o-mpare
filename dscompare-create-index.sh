PLATFORM=$(uname)
if [[ $PLATFORM == "Linux" ]]
then
	MD5CMD='md5sum'
else
	MD5CMD='md5'
fi

find $1 | while read line
do
	if [[ -f "$line" ]]
	then
		fileMd5=$($MD5CMD $line|cut -f 1 -d' ')
	else	
		fileMd5=00000000000000000000000000000000
	fi
	stat -c $fileMd5,%F,%i,%n $line

done
#; xargs -0 -l md5sum 
