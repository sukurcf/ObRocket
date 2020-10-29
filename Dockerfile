FROM rackspacedot/python38
WORKDIR /app
EXPOSE 5000
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @angular/cli
RUN git clone https://github.com/sukurcf/ORocket.git /app
CMD ["python", "process_basket.py"]