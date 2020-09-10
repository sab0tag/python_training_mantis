from sys import maxsize


class Project:

    def __init__(self, id=None, name=None, status=None, viewstatus=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.viewstatus = viewstatus
        self.description = description


    def __repr__(self):
        return "%s:%s:%s:%s:%s" % (self.id, self.name, self.status, self.viewstatus, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name and self.status == other.status \
               and self.viewstatus == other.viewstatus and self.description == other.description

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
