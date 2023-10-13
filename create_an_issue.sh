curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/MQueiros/github-workshop/issues \
  -d '{"title":"Found a bug","body":"I'\''m having a problem with this.","assignees":["MQueiros"],"labels":["bug"]}'