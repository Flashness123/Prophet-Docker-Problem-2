FROM python:3.7
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip setuptools wheel
#RUN python -m pip install -r requirements_proph.txt
RUN python -m pip install -r requirements.txt
EXPOSE 5000
EXPOSE 7321
EXPOSE 8000
CMD ["python", "api/app.py"] 