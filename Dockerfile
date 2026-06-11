FROM python:3.12

LABEL maintainer="pdbegroup"

WORKDIR /pdbe_api_tutorial

COPY ./requirements.txt /pdbe_api_tutorial/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["jupyter", "lab", "--allow-root", "--IdentityProvider.token=", "--ServerApp.password=", "--ip", "0.0.0.0", "--port", "8888", "--no-browser", "--ServerApp.root_dir=/pdbe_api_tutorial/pdbe_tutorial"]
