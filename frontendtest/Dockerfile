FROM cypress/browsers:chrome65-ff57

RUN npm install --save-dev cypress
RUN $(npm bin)/cypress verify

COPY . .