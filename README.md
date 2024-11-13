# Hydroponics-
 an automated data pipeline that integrates with a Google Drive folder. This pipeline  should monitor the folder for new data (e.g., sensor readings, images), process it  automatically, and update a simple visualization or dashboard to show the latest  conditions of a hydroponic system. 
#---- Instruction ----#

## Ngrok Setup and Usage ##

    ### What is Ngrok? ###
    Ngrok is a too that creates a secure tunnel between your local development environment and the public internet. We use it to: 
    - Create a public URL for testing our webhooks during development 
    - Allow external services to sned data to our locally running application
    - Test webhook integrations without deploying to a production server. 

    ### Installation Steps ###
    1. Download ngrok from https://ngrok.com/download
    2. Create a free ngrok account
    3. Follow the setup instructions provided after signing up

    ### Basic Usage ###
    1. Start your local application
    2. Open a terminal/command prompt
    3. Run: `ngrok http [port-number]`
    - Replace [port-number] with the port your application is running on
    4. Copy the generated URL to access your application

## Main Program Usage ##
    # Run the main file: main.py
    - After running, it will prompt you to enter the ngrok HTTPS address.
    - Ensure that the "data" and "images" folders (with files in them) are present in your directory.
    If these folders or files are missing, run detector.py independently to set them up and can stop once all files are downloaded.
    - Running detector.py will also prompt you for the ngrok HTTPS address.

    
    Required pip installs
     concurrent-futures
     flask
     Pillow
     watchdog
     google-api-python-client
     google-auth-httplib2
     google-auth-oauthlib
     
