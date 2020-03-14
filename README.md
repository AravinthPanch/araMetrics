# araMetrics
araMetrics is a personal impact measurement system to track metrics such as Awards, Connections, Earnings, Emissions, Events, Expenses, Learnings, Match-Makings, Meetings, Minutes, Practices, Projects, Purchases, Tasks, Teachings, Trips

## Setup
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```
pip freeze > requirements.txt
```

## Clockify
- API Documentation
  - https://clockify.me/developers-api

- API Tests
  - Get complete user details
  ```
  curl -H "content-type: application/json" -H "X-Api-Key: API_KEY" -X GET https://api.clockify.me/api/v1/user
  ```

  - Get list of workspaces
  ```
  curl -H "content-type: application/json" -H "X-Api-Key: API_KEY" -X GET https://api.clockify.me/api/workspaces/ > workspaces.log
  ```

  - Get list of projects
  ```
  curl -H "content-type: application/json" -H "X-Api-Key: API_KEY" -X GET https://api.clockify.me/api/workspaces/WORKSPACE_ID/projects/ > projects.log
  ```

  - Get list of tags
  ```
  curl -H "content-type: application/json" -H "X-Api-Key: API_KEY" -X GET https://api.clockify.me/api/workspaces/WORKSPACE_ID/tags/ > tags.log
  ```
