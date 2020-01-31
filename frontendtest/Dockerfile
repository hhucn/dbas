FROM cypress/browsers:chrome69

RUN npm install --save-dev cypress
RUN $(npm bin)/cypress verify

COPY . .