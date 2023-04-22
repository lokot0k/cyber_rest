make compose-up
sleep 2
make compose-exec cmd='make migrate-up'
