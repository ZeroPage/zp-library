import connexion

app = connexion.App(__name__, specification_dir='swagger/', swagger_ui=True)
app.add_api('swagger.yaml')
APPLICATION = app.app
