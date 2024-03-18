template = {
  "swagger": "2.0",
  "info": {
    "title": "SklepZoo",
    "description": "API for ecommerce",
    "contact": {
      "responsibleOrganization": "",
      "responsibleDeveloper": "",
      "email": "bartass97@gmail.com",
      "url": "https://github.com/PrzybyszB",
    },
    "termsOfService": "https://github.com/PrzybyszB",
    "version": "1.0"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
            "static_path": "/home/pbartosz/Programowanie/Projekty/Sklep_zoo/src/docs",
            "swagger_ui": True,
            "specs_route": "/apidocs/"
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}


