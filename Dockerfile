FROM rackspacedot/python38
WORKDIR /app
EXPOSE 5000
EXPOSE 4200
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @angular/cli
RUN ["git", "clone", "https://github.com/sukurcf/ObRocket.git", "/app"]
RUN ["git", "clone", "https://github.com/sukurcf/ObRocket-UI.git", "/webapp"]
RUN ["pip", "install", "-r", "requirements.txt"]
RUN cd /webapp && npm i && cd /app
RUN ["chmod", "+x", "/app/entrypoint.sh"]
CMD ["./entrypoint.sh"]