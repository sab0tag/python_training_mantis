from selenium.webdriver.support.ui import Select
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        driver = self.app.driver
        if not (driver.current_url.endswith("manage_proj_page.php")):
            driver.find_element_by_link_text("Manage").click()
            driver.find_element_by_link_text("Manage Projects").click()

    def change_field_value(self, field_name, text):
        driver = self.app.driver
        if text is not None:
            driver.find_element_by_name(field_name).click()
            driver.find_element_by_name(field_name).clear()
            driver.find_element_by_name(field_name).send_keys(text)

    def change_option_value(self, field_name, option):
        driver = self.app.driver
        if option is not None:
            driver.find_element_by_name(field_name).click()
            Select(driver.find_element_by_name(field_name)).select_by_visible_text(option)

    def fill_project_form(self, project):
        driver = self.app.driver
        self.change_field_value("name", project.name)
        self.change_option_value("status", project.status)
        self.change_option_value("view_state", project.viewstatus)
        self.change_field_value("description", project.description)

    def get_projects_lst(self):
        driver = self.app.driver
        self.open_project_page()
        proj_table = driver.find_elements_by_tag_name("table")[2]
        proj_rows = proj_table.find_elements_by_tag_name("tr")[2:]
        get_proj_lst = []
        for element in proj_rows:
            cells = element.find_elements_by_tag_name("td")
            id_ = cells[0].find_element_by_tag_name("a").get_attribute("href").replace(
                "http://localhost/mantis/manage_proj_edit_page.php?project_id=", "")
            name = cells[0].find_element_by_tag_name("a").text
            status = cells[1].text
            viewstatus = cells[3].text
            description = cells[4].text
            get_proj_lst.append(Project(id=id_, name=name, status=status, viewstatus=viewstatus, description=description))
        return get_proj_lst

    def create_project(self, project):
        driver = self.app.driver
        self.open_project_page()
        driver.find_element_by_xpath("//input[@type='submit' and @value='Create New Project']").click()
        self.fill_project_form(project)
        driver.find_element_by_xpath("//input[@value='Add Project']").click()

    def delete_project(self, id):
        driver = self.app.driver
        self.open_project_page()
        self.select_project_by_id(id)
        driver.find_element_by_xpath("//input[@type='submit' and @value='Delete Project']").click()
        if driver.current_url.endswith("/manage_proj_delete.php"):
            driver.find_element_by_xpath("//input[@type='submit' and @value='Delete Project']").click()
        self.back_to_the_main_page()

    def select_project_by_id(self, id):
        driver = self.app.driver
        driver.find_element_by_css_selector("tr:nth-child(n+3) > td:nth-child(n) > a").click()

    def back_to_the_main_page(self):
        driver = self.app.driver
        driver.get("http://localhost/mantis/my_view_page.php")
