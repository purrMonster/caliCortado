FROM denoland/deno:2.6.9@sha256:2221eafd8a7556693307ad9889a79d4974e1844a6964acbe466ab9faa15d37bf
WORKDIR /app
RUN chown deno:deno /app
USER deno
# Build context must be the clean, pinned upstream checkout verified by run.py.
COPY --chown=deno:deno . .
RUN deno install --frozen && deno cache --frozen main.ts Peer.test.ts PeerStorage.test.ts types.test.ts util.test.ts test/integration/PeerCouchDB.integration.ts
