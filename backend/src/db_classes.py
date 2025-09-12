from app import db

class BusinessUnit(db.Model):
    __tablename__ = 'business_unit'
    alias = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    def json(self):
        return {
            'alias': self.bu_alias,
            'bu_name': self.bu_name
        }

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'business_unit': self.business_unit,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
class Parameter(db.Model):
    __tablename__ = 'parameter'
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False, primary_key=True)
    value = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    is_notified = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'value': self.value,
            'is_notified': self.is_notified
        }

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')            
        }
    
class PNLCategory(db.Model):
    __tablename__ = 'pnl_category'
    code = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=True)

    def json(self):
        return {
            'code': self.id,
            'name': self.name,
            'description': self.description
        }
    
class PNLRecord(db.Model):
    __tablename__ = 'pnl_record'
    code = db.Column(db.String(15), db.ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 2), nullable=False)

    def json(self):
        return {
            'code': self.code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%Y-%m'),
            'value': self.value
        }
    
class PNLForecast(db.Model):
    __tablename__ = 'pnl_forecast'
    code = db.Column(db.String(15), db.ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 2), nullable=False)

    def json(self):
        return {
            'code': self.code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%Y-%m'),
            'value': self.value
        }