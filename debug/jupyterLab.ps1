cd F:\docker\dcpy
docker run -v $PWD/opt:/root/opt -v F:\Data:/root/data -w /root -it --rm -p 7777:8888 dcpy-flask jupyter-lab --ip 0.0.0.0 --allow-root -b localhost