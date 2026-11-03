#!/bin/bash
# Builds site/ into dist/ with the real domain, then deploys dist/ to the
# Hostinger docroot defined in .env.
# Usage: bash scripts/deploy.sh          (add/update files only)
#        DEPLOY_DELETE=1 bash scripts/deploy.sh   (also prune remote files missing locally)
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "ERROR: .env not found. Copy .env.example to .env and fill in your SSH details." >&2
  exit 1
fi
set -a
source .env
set +a

: "${SSH_HOST:?SSH_HOST missing in .env}"
: "${SSH_PORT:?SSH_PORT missing in .env}"
: "${SSH_USER:?SSH_USER missing in .env}"
: "${SSH_PASSWORD:?SSH_PASSWORD missing in .env}"
: "${REMOTE_PATH:?REMOTE_PATH missing in .env}"
: "${DOMAIN:?DOMAIN missing in .env}"

# Refuse to deploy while .env still holds the template placeholders.
if [ "$SSH_HOST" = "your.server.ip" ] || [ "$SSH_USER" = "u000000000" ] || \
   [ "$SSH_PASSWORD" = "your-password-here" ] || [ "$DOMAIN" = "yourdomain.com" ] || \
   [[ "$REMOTE_PATH" == *yourdomain.com* ]]; then
  echo "ERROR: .env still contains template values. Add your real domain and Hostinger SSH details first." >&2
  exit 1
fi

if [ ! -f site/index.html ]; then
  echo "ERROR: site/index.html not found. Build the site before deploying." >&2
  exit 1
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "ERROR: Python 3 is needed to run scripts/build.py." >&2
  exit 1
fi
"$PY" scripts/build.py --require-domain

export SSHPASS="$SSH_PASSWORD"
export DEPLOY_DELETE="${DEPLOY_DELETE:-0}"
export SSH_HOST SSH_PORT SSH_USER REMOTE_PATH

echo "Deploying dist/ -> $SSH_USER@$SSH_HOST:$REMOTE_PATH (delete mode: $DEPLOY_DELETE)"

/usr/bin/expect <<'EXPECT_EOF'
set timeout 300
set pass $env(SSHPASS)
set cmd [list rsync -av --exclude .DS_Store]
if {$env(DEPLOY_DELETE) eq "1"} { lappend cmd --delete }
lappend cmd -e "ssh -p $env(SSH_PORT) -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no"
lappend cmd dist/ "$env(SSH_USER)@$env(SSH_HOST):$env(REMOTE_PATH)/"
spawn {*}$cmd
expect {
    -re "(?i)password" { send "$pass\r"; exp_continue }
    eof
}
catch wait result
exit [lindex $result 3]
EXPECT_EOF

echo ""
echo "Verifying https://$DOMAIN/ ..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -m 30 "https://$DOMAIN/" || echo "unreachable")
echo "https://$DOMAIN/ -> HTTP $STATUS"
