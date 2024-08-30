# GitHubActions



```markdown
# Flask ML Application Deployment to Azure

This repository contains a Flask-based machine learning (ML) application that is deployed to Azure using GitHub Actions. This guide will help you set up and automate the deployment process.

## Azure Setup & Prerequisites

- Azure Account: Create an Azure account if you don't have one.
- GitHub Repository: Your Flask application should be in a GitHub repository.
- Create Resource Group: Create your Resource Group
- Create Container Registry: For Holding Docker Images
- Go to Resources, Find Access Key, Enable Admin User and Copy password
- Create Web App: Publish -> Choose Container -> Change Image Source to Azure Container Registry (Follow this step After Pushing the Image) 

## Application Setup

1. Flask Application: Ensure you have a Flask application with a `requirements.txt` for dependencies.

   Example directory structure:
   ```
   my_flask_app/
   ├── app.py
   ├── requirements.txt
   ├── Dockerfile
   └── .gitignore
   ```

2. Dockerize Your Application: Create a `Dockerfile` for containerizing your Flask application.

   Example `Dockerfile`:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt

   COPY . .

   CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
   ```

3. Create Docker image and Push to Azure Container Repository
  ```
  docker build -t bitscontainerregistry.azurecr.io/diabetes_prediction_app:latest .

  docker login bitscontainerregistry.azurecr.io

  docker push bitscontainerregistry.azurecr.io/diabetes_prediction_app:latest


  ```


## GitHub Actions Setup

1. **Create GitHub Action Workflow**:

   In your GitHub repository, create a directory `.github/workflows` if it doesn’t exist. Inside it, create a file `deploy.yml`.

   Example `deploy.yml`:
   ```yaml
   name: Build and Deploy Flask App

   on:
     push:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout code
           uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: 3.9

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt

         - name: Build Docker image
           run: |
             docker build . -t my-flask-app

         - name: Log in to Azure Container Registry
           uses: azure/docker-login@v1
           with:
             login-server: myContainerRegistry.azurecr.io
             username: ${{ secrets.ACR_USERNAME }}
             password: ${{ secrets.ACR_PASSWORD }}

         - name: Push Docker image to ACR
           run: |
             docker tag my-flask-app myContainerRegistry.azurecr.io/my-flask-app:latest
             docker push myContainerRegistry.azurecr.io/my-flask-app:latest

         - name: Deploy to Azure Web App
           uses: azure/webapps-deploy@v2
           with:
             app-name: myFlaskApp
             slot-name: production
             images: myContainerRegistry.azurecr.io/my-flask-app:latest
   ```

2. **Configure GitHub Secrets**:

   Go to your GitHub repository settings, and add the following secrets:

   - `ACR_USERNAME`: The username for your Azure Container Registry.
   - `ACR_PASSWORD`: The password for your Azure Container Registry.

   You can find these credentials in the Azure portal under the Access Keys section of your ACR.

3. **Commit and Push**: Commit your changes and push them to GitHub. This should trigger the GitHub Action workflow, which builds and deploys your Flask application.

   ```bash
   git add .
   git commit -m "Add GitHub Actions workflow for deployment"
   git push origin main
   ```

## Conclusion

This guide provides a basic setup for deploying a Flask ML application to Azure using GitHub Actions. Adjust the details according to your specific application requirements and environment. If you encounter issues, check the GitHub Actions logs for troubleshooting and ensure that all Azure and Docker credentials are correctly configured.

For more information, refer to the [Azure Documentation](https://docs.microsoft.com/en-us/azure/) and [GitHub Actions Documentation](https://docs.github.com/en/actions).

```