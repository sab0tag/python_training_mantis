import random
from model.project import Project


def test_create_project(app):
    project = Project(name="name-" + str(random.randrange(100)),
                      status=random.choice(["development", "release"]),
                      viewstatus=random.choice(["private", "public"]),
                      description="description-" + str(random.randrange(100)))
    app.session.login("administrator", "root")
    # old_projects_lst = app.project.get_projects_lst()
    old_projects_lst = app.soap.get_projects_lst("administrator", "root")
    app.project.create_project(project)
    # new_projects_lst = app.project.get_projects_lst()
    new_projects_lst = app.soap.get_projects_lst("administrator", "root")
    old_projects_lst.append(project)
    assert sorted(old_projects_lst, key=Project.id_or_max) == sorted(new_projects_lst, key=Project.id_or_max)
