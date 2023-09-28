from common.model import db
from contextlib import contextmanager


class Base:
    model = None

    def first(self, filters):
        """ returns first element of the query """
        query = self.model.query
        query = query.filter(self.model.is_not_deleted)
        return query.filter_by(**filters).first()

    def first_or_404(self, filters):
        """ Like :meth:`first` but aborts with 404 if not found instead of returning ``None``. """
        query = self.model.query
        query = query.filter(self.model.is_not_deleted)

        return query.filter_by(**filters).first_or_404()

    @staticmethod
    def commit(obj):
        """
        commits the obj to database
        :param obj:
        :return:
        """
        db.session.add(obj)
        db.session.commit()
        return

    @staticmethod
    def bulk_commit(objs):
        """
        bulk commit the list of objects to database.
        :param objs:
        :return:
        """
        for obj in objs:
            db.session.add(obj)

        db.session.commit()
        return True

    @staticmethod
    def update_commit():
        """
        commit the current updated transaction
        @return:
        """
        db.session.commit()
        return

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        try:
            yield db.session
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception("Error in session_scope")
        finally:
            db.session.close()