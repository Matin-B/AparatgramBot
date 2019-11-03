FROM python:latest
COPY app.py .
COPY Aparat.py .
RUN pip3 install python-telegram-bot --upgrade
RUN pip3 install bs4 --upgrade
RUN pip3 install requests --upgrade
RUN pip3 install uuid --upgrade
ENTRYPOINT [ "python3" ]
CMD ["app.py"] 
