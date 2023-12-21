#Base OS
FROM python:alpine3.19

#Moving python modules to network_dsl directory
COPY . /network_dsl

#Change directory to bin
WORKDIR /bin

#Grab a version of yang2dsdl from github
RUN wget 'https://raw.githubusercontent.com/mbj4668/pyang/master/bin/yang2dsdl'

#modify file permissions so yang2dsdl can be ran
RUN chmod 755 yang2dsdl

#install required libraries for yang2dsdl
RUN apk add libxslt \
    libxml2-utils

#Change directory to network_dsl
WORKDIR /network_dsl

#Install python requirements
RUN pip install -r requirements.txt



