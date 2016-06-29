# $1 being the user@server_ip_address and $2 being ip of path to deploy script
check_if_success(){
    if [ $? -ne 0 ]; then
        echo "error occured"
        exit
    else
        echo "command successfull"
    fi
}
ssh -T -i $1 $2
check_if_success
$3