FROM node:20-alpine

# git-raw-commits / git-semver-tags shell out to the real git binary
RUN apk add --no-cache git

# The container runs as root while the bind-mounted repo is owned by the host
# user, which trips git's "dubious ownership" protection (CVE-2022-24765) the
# moment it tries to read history. /app is always where this image's mount
# point lands (see WORKDIR below), so it's always safe to trust here.
RUN git config --system --add safe.directory /app

RUN npm install -g gitmoji-changelog@2.3.0

WORKDIR /app
ENTRYPOINT ["gitmoji-changelog"]
