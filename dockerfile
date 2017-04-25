#pull latest image
FROM gcr.io/tensorflow/tensorflow
# MAKE folder and set
RUN mkdir /tf_files
WORKDIR /tf_files
# copy model file
COPY . .

CMD bash