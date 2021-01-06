from main import db


class SeasonalD(db.Model):
    __tablename__ = "seasonalds"
    
    id = db.Column(db.Integer, primary_key=True)
    seasonald_title = db.Column(db.String())
    
    def __repr__(self):
        return f"<Artist {self.seasonald_title}>"