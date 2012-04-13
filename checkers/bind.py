from base import Base

class Bind(Base):
    _bind_list = ['bind9']
    def do_check(self, pkg):
        if pkg in self._bind_list:
            return 'bind_checker'
        else:
            return []
