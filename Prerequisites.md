## Prerequisites

- [Prerequisites](#prerequisites)
  - [Tooling](#tooling)
  - [Clone this Repo](#clone-this-repo)
  - [Create Local Virtual Python Environment](#create-local-virtual-python-environment)
  - [Python Modules](#python-modules)
  - [Powershell Modules](#powershell-modules)
  - [Setup Environment Variables](#setup-environment-variables)
  - [Create Application Registration and Add to Environment Variables](#create-application-registration-and-add-to-environment-variables)

### Tooling

You will need to ensure you have an Azure account with a subscription that you can use. You could use your MSDN subscription if you have one or you can sign up for a free trial using the link below.

- [Azure Subscription](https://azure.microsoft.com/en-gb/free/)

Please ensure you have the following tools installed on your machine.

- [Visual Studio Code](https://code.visualstudio.com/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)
- [Bicep VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
- [Bicep CLI](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/install#windows)
- [Event Hub VS Code](https://marketplace.visualstudio.com/items?itemName=Summer.azure-event-hub-explorer)
- [Powershell VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.PowerShell)
- [Python](https://www.python.org/downloads/)
  - Here is a good [tutorial](https://www.youtube.com/watch?v=QYTPpqPYaw0&t=14s) on how to install python along with spark and pyspark which is useful for data streaming pipelines.

### Clone this Repo

To utilise the code in this repo, clone it from gihub and then open it up in Visual Studio code.

### Create Local Virtual Python Environment

1. Open your Visual Studio code terminal.
2. Ensure you are in the root of the azure_eventdrivenarchitecture repo.
3. Run the following to create a virtual environment called venv.

```cmd
python -m venv venv
```

**Important Note** : We will be using a single virtual environment for this entire implementation, but remember we are actually imitating a number of teams so the environment should actually be split per each teams implementation and what packages and dependencies they need along to carry out their function.

3. Activate the python environment by running the following.

```cmd
venv\scripts\activate
```

4. To deactivate the python environment at any time run the following.

```cmd
venv\scripts\deactivate
```

### Python Modules

To complete all of the scenarios in this azure_eventdrivenarchitecture you need to activate your environment and install the following packages.

1. First activate your environment.

```py
venv\scripts\activate
```

2. Then pip install the required packages.

```bash
pip install avro                       
pip install azure-common            
pip install azure-core           
pip install azure-cosmos             
pip install azure-eventhub        
pip install azure-functions         
pip install azure-identity            
pip install azure-keyvault-secrets  
pip install pip install azure-schemaregistry         
pip install azure-schemaregistry-avroserializer
pip install azure-storage-blob
pip install Faker
```

3. You can confirm the packages you have installed by running the following.

```cmd  
pip list
```

**Remember:** As mentioned above we are imitating a number of teams in this architecture and only creating one environment for all the packages for simplicity. In reality each team or implementation woud have only its own required libraries installed for its specific virtual environment.

### Powershell Modules

1. You will need the suite of [az powershell modules](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-7.1.0) for some of the deployment exercises. To install these run the following in a powershell terminal.

```ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
```

### Setup Environment Variables

Throughout the course you will be utilising a number of variables repeatedly, and it is easier to store them in environment variables so that they can be referenced consistently.

They are:

- **AZURE_UNIQUE_NAMESPACE** - This will be the unique postfix you apply to all your Azure resources to ensure they are globally unique.
- **AZURE_SUBSCRIPTION** - This will be the name of the Azure subscription you are working in.
- **AZURE_REGION** - This will be the name of the Azure region you are working in.

1. Open your system environment variables on your machine.
2. Add a unique namespace for your azure resources using the AZURE_UNIQUE_NAMESPACE variable name with an appropriate value. For example mine is "dgrf".
3. Add the name of the azure subscription you are going to be using the AZURE_SUBSCRIPTION as the variable name. For example mine is "dataGriff teaching".
4. Add the name of the azure subscription you are going to be using the AZURE_REGION variable name. For example mine is "northeurope".
5. Your system environment variables should now look something like this.
![Environment Variables](/Images/EnvironmentVariables.PNG)
6. Once you have set your environment variable you will need to restart your IDE (Visual Studio Code) to pick up the new values.

Throughout the code these system variables will be referenced like the examples below.

Like this in Powershell...

```ps1
[System.Environment]::GetEnvironmentVariable('AZURE_UNIQUE_NAMESPACE')
```

Like this in Python...

```py
unique_namespace = os.environ.get('AZURE_UNIQUE_NAMESPACE')
```

Like this in command line...

```cmd
"%AZURE_UNIQUE_NAMESPACE%"
```

**Important Help** - When using the environment variables and switching languages, your values may get in a bit of a twist on occassion. If you do get any errors I recommend just killing all terminals, restarting visual studio code and starting from scratch.

### Create Application Registration and Add to Environment Variables

We are going to be creating an application registration that we will use for the majority of our authentication against our new estate for the following exercises. We will also store these credentials in our system environment variables.

1. In the Azure Portal go into application registrations in Azure Active directory (you can also find a link to this on your dashboard in the markdown on the left).
2. Create a new app registration called aprg-events-admin.

![App Reg](/Images/AppReg.PNG)

We are now going to store the credentials of the application registration created above in our local environment variables. These values will be used whenever we reference the below sections of code in our python scripts as per this [online documentation](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#environment-variables).

```py
from azure.identity._credentials.default import DefaultAzureCredential
...
token_credential = DefaultAzureCredential()
```

1. Edit the environment variables for your account on your local machine.
2. First add a variable for AZURE_CLIENT_ID from your new application registration.
3. Then add a variable for AZURE_TENANT_ID from your new application registration.
4. Next we need to generate a secret from our application registration and add this to our environment variables.
5. Once you have copied this value, paste it into a new local environment variable called AZURE_CLIENT_SECRET.

![Environment Variables App Reg](/Images/EnvironmentVariablesAppReg.PNG)
