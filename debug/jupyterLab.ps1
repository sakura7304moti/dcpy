cd F:\docker\flask-server
docker run -v $PWD/opt:/root/opt -v F:\Data:/root/data -w /root -it --rm -p 7777:8888 flask-server-flask jupyter-lab --ip 0.0.0.0 --allow-root -b localhost