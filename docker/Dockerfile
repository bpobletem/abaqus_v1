# Build using the project root as the build context, for example:
#   docker build -f docker/Dockerfile -t abaqus_v1 .
FROM python:3.13

COPY requirements/ requirements/
RUN pip install -r requirements/base.txt

RUN mkdir /app
WORKDIR /app
ADD ./ /app/