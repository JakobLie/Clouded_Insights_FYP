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
            'created_at': self.created_at.strftime('%d-%m-%Y %H:%M:%S')
        }
    
    def authenticate(self, password):
        if (password == self.password_hash):
            return True
        return False

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'type': self.type,
            'subject': self.subject,
            'body': self.body,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%d-%m-%Y %H:%M:%S')
        }
    
class PNLCategory(db.Model):
    __tablename__ = 'pnl_category'
    code = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_code = db.Column(db.String(15), db.ForeignKey('pnl_category.code'), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def json(self):
        return {
            'code': self.code,
            'name': self.name,
            'parent_code': self.parent_code,
            'description': self.description
        }
    
class PNLEntry(db.Model):
    __tablename__ = 'pnl_entry'
    pnl_code = db.Column(db.String(15), db.ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 2), nullable=False)

    def json(self):
        return {
            'pnl_code': self.pnl_code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value)
        }
    
class PNLForecast(db.Model):
    __tablename__ = 'pnl_forecast'
    pnl_code = db.Column(db.String(15), db.ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 2), nullable=False)

    def json(self):
        return {
            'pnl_code': self.pnl_code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value)
        }
    
class Parameter(db.Model):
    __tablename__ = 'parameter'
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'), primary_key=True)
    kpi_alias = db.Column(db.String(10), db.ForeignKey('kpi_category.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 4), nullable=False)
    is_notified = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'employee_id': self.employee_id,
            'kpi_alias': self.kpi_alias,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value),
            'is_notified': self.is_notified
        }
    
class KPICategory(db.Model):
    __tablename__ = 'kpi_category'
    alias = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def json(self):
        return {
            'alias': self.alias,
            'name': self.name,
            'category': self.category,
            'description': self.description
        }

class KPIEntry(db.Model):
    __tablename__ = 'kpi_entry'
    kpi_alias = db.Column(db.String(10), db.ForeignKey('kpi_category.alias'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 4), nullable=False)

    def json(self):
        return {
            'kpi_alias': self.kpi_alias,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value)
        }
    
class KPIForecast(db.Model):
    __tablename__ = 'kpi_forecast'
    kpi_alias = db.Column(db.String(10), db.ForeignKey('kpi_category.alias'), primary_key=True)
    business_unit = db.Column(db.String(10), db.ForeignKey('business_unit.alias'), primary_key=True)
    month = db.Column(db.Date, primary_key=True)
    value = db.Column(db.Numeric(15, 4), nullable=False)

    def json(self):
        return {
            'kpi_alias': self.kpi_alias,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value)
        }