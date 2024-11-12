FROM python:3.10

WORKDIR /pdbe_api_tutorial

COPY ./requirements.txt /pdbe_api_tutorial/requirements.txt 
 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

COPY ./pdbe_tutorial_2024 /pdbe_api_tutorial/pdbe_tutorial_2024

CMD ["jupyter-server", "--allow-root", "--ip", "0.0.0.0", "--port", "8888", "--no-browser", "pdbe_tutorial_2024/"]
