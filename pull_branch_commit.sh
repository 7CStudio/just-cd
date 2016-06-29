check_if_success(){
    if [ $? -ne 0 ]; then
        echo "error occured"
        exit
    else
        echo "command successfull"
    fi
}

pull_code(){
    git checkout -b $1
    git pull origin $1
    git checkout $2
    check_if_success
}
cd $1
pull_code $2 $3