FROM rackspacedot/python38
WORKDIR /app
EXPOSE 5000
RUN git clone https://github.com/sukurcf/ORocket.git /app
CMD ["python", "process_basket.py"]