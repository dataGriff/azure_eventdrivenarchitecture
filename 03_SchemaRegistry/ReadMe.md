Ensure PATH in system variables has path to python!

Forwards compatibility for the win
[Compatibility](https://stevenheidel.medium.com/backward-vs-forward-compatibility-9c03c3db15c9#:~:text=Backward%20compatibility%20means%20that%20readers,writers%20with%20a%20newer%20schema.)

```
python -m venv venv
```

```
venv\scripts\activate
```

```
pip install azure-schemaregistry-avroserializer azure-identity
pip install azure-schemaregistry azure-identity
```

Create app reg aprg-events-admin
Give admin access on all your new event resource groups
Add to your user environment variables
[Defaut Environment Vars](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#environment-variables)