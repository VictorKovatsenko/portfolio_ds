# app/Dockerfile
# Start with a base image
FROM python:3-onbuild
# Copy our application code
WORKDIR /var/app
COPY . .
COPY requirements.txt .
# Fetch app specific dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install XGBoost library
#RUN git clone --recursive https://github.com/dmlc/xgboost
RUN pip install --pre xgboost
#RUN mkdir build
#RUN cd build
#RUN cmake ..
#RUN make -j$(nproc)

# Expose port
EXPOSE 5000
# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]