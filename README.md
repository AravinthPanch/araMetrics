# araMetrics
araMetrics is a personal impact measurement system to track metrics such as Awards, Connections, Earnings, Emissions, Events, Expenses, Learnings, Match-Makings, Meetings, Minutes, Practices, Projects, Purchases, Tasks, Teachings, Trips

## Setup
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

- Save dependencie to requirements.txt
```
pip freeze > requirements.txt
```

- Install dependencie from requirements.txt
```
pip install -r requirements.txt
```

- Deply credentials to the server
```
scp credentials.json keys.py aravinth.info:~/
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
