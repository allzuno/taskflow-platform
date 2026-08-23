FROM node:22-alpine
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY app.js .
# MUST be numeric, not "USER node". The pod securityContext sets
# runAsNonRoot: true, and the kubelet cannot verify a *named* user is
# non-root -- it rejects the pod with "image has non-numeric user".
# 1000 is the uid of the built-in `node` user in the official image.
USER 1000
EXPOSE 5001
# busybox wget IS present in alpine, so no extra install needed here
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
 CMD wget -q --spider http://localhost:5001/health || exit 1
CMD ["npm", "start"]
