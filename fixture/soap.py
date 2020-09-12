from suds.client import Client
from suds import WebFault
from fixture.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantis/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_lst(self, username, password):
        client = Client("http://localhost/mantis/api/soap/mantisconnect.php?wsdl")
        client.service.mc_projects_get_user_accessible(username, password)
        try:
            projects_data = client.service.mc_projects_get_user_accessible(username, password)
            projects_lst = []
            for itm in projects_data:
                project = Project(id=itm.id, name=itm.name, status=itm.status.name, viewstatus=itm.view_state.name,
                                  description=itm.description)
                projects_lst.append(project)
            return projects_lst
        except WebFault:
            return False
