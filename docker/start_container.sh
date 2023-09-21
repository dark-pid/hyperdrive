if [ ! "$(docker ps -a -q -f name=<name>)" ]; then
    docker stop hyperdrive-main
    docker rm hyperdrive-main

    if [ "$(docker ps -aq -f status=exited -f name=<name>)" ]; then
        # cleanup
        docker rm <name>
    fi
fi

# run your container
docker run -dp 5001:8080 --name hyperdrive-main hyperdrive-main
