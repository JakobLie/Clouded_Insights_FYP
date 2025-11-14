from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, String, Numeric, Boolean, Integer, Text, Date, DateTime

base = declarative_base()

class BusinessUnit(base):
    __tablename__ = 'business_unit'
    alias = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=True)

    def json(self):
        return {
            'alias': self.alias,
            'bu_name': self.name
        }

class Employee(base):
    __tablename__ = 'employee'
    id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    role = Column(String(50), nullable=False)
    business_unit = Column(String(10), ForeignKey('business_unit.alias'), nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role,
            'business_unit': self.business_unit,
            'created_at': self.created_at.strftime('%d-%m-%Y %H:%M:%S')
        }
    
    def authenticate(self, password):
        if (password == self.password_hash):
            return True
        return False

class Notification(base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(20), ForeignKey('employee.id'), nullable=False)
    type = Column(String(50), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)

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
    
class PNLCategory(base):
    __tablename__ = 'pnl_category'
    code = Column(String(15), primary_key=True)
    name = Column(String(100), nullable=False)
    parent_code = Column(String(15), ForeignKey('pnl_category.code'), nullable=True)
    description = Column(Text, nullable=True)
    trend = Column(String(50), nullable=False, default='STATIC')

    def json(self):
        return {
            'code': self.code,
            'name': self.name,
            'parent_code': self.parent_code,
            'description': self.description,
            'trend': self.trend
        }
    
class PNLEntry(base):
    __tablename__ = 'pnl_entry'
    pnl_code = Column(String(15), ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = Column(String(10), ForeignKey('business_unit.alias'), primary_key=True)
    month = Column(Date, primary_key=True)
    value = Column(Numeric(15, 2), nullable=True)
    pnl_category = relationship('PNLCategory', backref='entries')

    def json(self):
        return {
            'pnl_code': self.pnl_code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value) if self.value is not None else None
        }
    
class PNLForecast(base):
    __tablename__ = 'pnl_forecast'
    pnl_code = Column(String(15), ForeignKey('pnl_category.code'), primary_key=True)
    business_unit = Column(String(10), ForeignKey('business_unit.alias'), primary_key=True)
    month = Column(Date, primary_key=True)
    value = Column(Numeric(15, 2), nullable=True)

    def json(self):
        return {
            'pnl_code': self.pnl_code,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value) if self.value is not None else None
        }
    
class KPICategory(base):
    __tablename__ = 'kpi_category'
    alias = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    def json(self):
        return {
            'alias': self.alias,
            'name': self.name,
            'category': self.category,
            'description': self.description
        }
    
class Parameter(base):
    __tablename__ = 'parameter'
    employee_id = Column(String(20), ForeignKey('employee.id'), primary_key=True)
    kpi_alias = Column(String(10), ForeignKey('kpi_category.alias'), primary_key=True)
    month = Column(Date, primary_key=True)
    value = Column(Numeric(15, 4), nullable=True)
    is_notified = Column(Boolean, default=False)

    def json(self):
        return {
            'employee_id': self.employee_id,
            'kpi_alias': self.kpi_alias,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value) if self.value is not None else None,
            'is_notified': self.is_notified
        }

class KPIEntry(base):
    __tablename__ = 'kpi_entry'
    kpi_alias = Column(String(10), ForeignKey('kpi_category.alias'), primary_key=True)
    business_unit = Column(String(10), ForeignKey('business_unit.alias'), primary_key=True)
    month = Column(Date, primary_key=True)
    value = Column(Numeric(15, 4), nullable=True)

    def json(self):
        return {
            'kpi_alias': self.kpi_alias,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value) if self.value is not None else None
        }
    
class KPIForecast(base):
    __tablename__ = 'kpi_forecast'
    kpi_alias = Column(String(10), ForeignKey('kpi_category.alias'), primary_key=True)
    business_unit = Column(String(10), ForeignKey('business_unit.alias'), primary_key=True)
    month = Column(Date, primary_key=True)
    value = Column(Numeric(15, 4), nullable=True)

    def json(self):
        return {
            'kpi_alias': self.kpi_alias,
            'business_unit': self.business_unit,
            'month': self.month.strftime('%m-%Y'),
            'value': float(self.value) if self.value is not None else None
        }