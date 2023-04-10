FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN python -m pip install jupyterlab
RUN python -m pip install snscrape
RUN python -m pip install selenium
RUN python -m pip install flask
RUN python -m pip install pandas
RUN python -m pip install Flask-Cors
RUN python -m pip install tqdm
RUN python -m pip install webdriver-manager
RUN python -m pip install PyDrive2
RUN python -m pip install yt_dlp
RUN python -m pip install moviepy
RUN python -m pip install timeout_decorator