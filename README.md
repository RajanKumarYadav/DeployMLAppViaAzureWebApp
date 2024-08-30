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

- Follow below step After Pushing the Image
- Create Web App: Publish -> Choose Container -> Change Image Source to Azure Container Registry  

## Application Setup

1. Flask Application: Ensure you have a Flask application with a `requirements.txt` for dependencies.

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
   Or Create using Azure Deployment Centre and choose proper repository

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