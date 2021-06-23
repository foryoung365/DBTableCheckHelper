# -*- coding: utf-8 -*-

import json
import os


PROJECTS_CONFIG = "projects.json"
CONFIG_FILENAME = "{project}_config.json"

class ProjectSelector:
    projects = {}
    project_selected = None

    def __init__(self) -> None:
        with open(PROJECTS_CONFIG, 'r', encoding="utf-8") as cfg:
            self.projects = json.load(cfg)["projects"]

    def getProjectNameList(self)->list:
        names = []
        for project in self.projects:
            names.append(project["name"])
        return names

    def setSelectedProject(self, name:str):
        for project in self.projects:
            if project["name"] == name:
                self.project_selected = project["project"]

    def getSelectedProjectName(self)->str:
        for project in self.projects:
            if project["project"] == self.project_selected:
                return project["name"]
    
    def getSelectedProject(self):
        return self.project_selected

    def getConfigFileName(self)->str:
        text = CONFIG_FILENAME.format(project=self.getSelectedProject())
        return text

    def isProjectConfigExists(self)->bool:
        filename = self.getConfigFileName()
        return os.path.exists(filename)
