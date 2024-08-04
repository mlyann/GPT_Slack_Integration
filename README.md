# Bot Integration Guide: ChatGPT with Slack

## Step 1: Create a Slack App

- Navigate to the **YourApps** page on Slack and sign in.
- Select **"Create New App"** or **"Create an App"** for first-time users.
- On the **"Create an app"** page, choose **"From scratch"**.
- On the **"Name app & choose workspace"** page:
  - Enter the name of your application.
  - Select the workspace for the application.
  - Agree to the Slack API terms of service and click **"Create App"**.
- After the app is created, go to the **"Basic Information"** page.
  - In the **"App Credentials"** section, copy and save the Client ID, Client Secret, and Signing Secret.

## Step 2: Add Permissions

- Visit the **"OAuth & Permissions"** page accessible from the sidebar.
- Under the **"Scopes"** section:
  - Click **"Add an OAuth Scope"** to include the following permissions:
    - `app_mentions:read`
    - `mpim:read`
    - `channels:history`
    - `im:history`
    - `channels:read`
    - `groups:read`
    - `chat:write`
    - `app_mentions:read`
  - Scroll to **"OAuth Tokens for Your Workspace"**, and click **"Install Workspace"**.
  - Review the workspace permissions, approve by clicking **"Allow"**, and save the Bot User OAuth Token.

  - Enable Event Subscriptions
  - Add these functions into:
    - `app_mention`
    - `message.im`

    
## Step 3: Configure Your Slack App

- Return to the **YourApps** page on Slack.
- Access **"OAuth & Permissions"**.
  - In the **"Redirect URLs"** section, click **"Add New Redirect URL"**. Enter the previously saved redirect URL and click **"Add"**, then **"Save URLs"**.
  - Enable bot event subscriptions by selecting **"Event Subscriptions"** and toggling **"Enable Events"**.
  - Enter the Event Request URL.
  - Expand **"Subscribe to bot events"**, click **"Add Bot User Event"**, and add events like `app_mentions` and `message.im`.
  - Set up slash commands by going to **"Slash Commands"**, click **"Create New Command"**.
  - Configure the command to `/clear_{appID}` (replace `{appID}` with your Slack Application ID).
  - Enter the Slash Request URL from the Coze configurations.

## Step 4: Publish and Test Your Bot

- Return to the code, we can build a ".env" file based on the following information.
- Build one ".env" file privately, customize the code as below:
  - SLACK_BOT_TOKEN=xoxb-... 
  - SLACK_APP_TOKEN=xapp-...
  - OPENAI_API_KEY=sk-proj-...


## Step 5: Deploy and Run Continuously on EC2


  In the EC2 (AWS), etc..

  Running this code: 

  Going to the root mode:

  ```
  sudo su
  ```

  Running the code command:

  ```
  nohup python3 my_script.py & 
  ```

  To check the status of the code, using:

  ```
  tail -f nohup.out
  ```

  Btw, if we want to stop that:

  1. we can going to

  ```
  ps aux | grep python3
  ```

  To check all status:

  ```
  root       14514  0.1  6.0 143016 58804 ?        Sl   14:12   0:01 python3 app.py
  root       15083  0.0  0.2   7008  2304 pts/1    S+   14:21   0:00 grep --color=auto python3
  ```

  Then we can use “kill + (id of program)” to stop app.py
  For example, 
  ```kill 14515``` 
  Killing the app.py program.


# Author:
  - Ming
