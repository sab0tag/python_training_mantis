import random
from model.project import Project


def test_delete_project(app):
    app.session.login("administrator", "root")
    if len(app.project.get_projects_lst()) == 0:
        app.project.create_project(Project(name="name-" + str(random.randrange(100)),
                                           status=random.choice(["development", "release"]),
                                           viewstatus=random.choice(["private", "public"]),
                                           description="description-" + str(random.randrange(100))))
    old_projects_lst = app.project.get_projects_lst()
    project = random.choice(old_projects_lst)
    app.project.delete_project(project)
    new_projects_list = app.project.get_projects_lst()
    assert old_projects_lst - 1 == new_projects_list
    old_projects_lst.remove(project)
    """
    old_projects_lst.remove(project)
    assert sorted(old_projects_lst, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
    """
