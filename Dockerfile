FROM python:3.11

# use tuna apt mirror
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# install dependencies
RUN apt-get update && apt-get install -y git fish

# use tuna pip mirror
RUN mkdir -p ~/.pip && echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf

# install pdm
RUN pip install pdm

# use fish as default shell
RUN chsh -s /usr/bin/fish

# keep container running
CMD ["tail", "-f", "/dev/null"]