import sqlalchemy as sa

metadata = sa.MetaData()

user = sa.Table('user', metadata,
                sa.Column('user_id', sa.Integer, primary_key=True),
                sa.Column('first_name', sa.String(255), nullable=False),
                sa.Column('last_name', sa.String(255), nullable=False),
                sa.Column('email', sa.String(255), nullable=False, unique=True),
                sa.Column('hash', sa.String(255), nullable=False),
                sa.Column('verification_code', sa.String(255), nullable=False),
                sa.Column('verified', sa.Boolean()),
                )


company = sa.Table('company', metadata,
                   sa.Column('company_id', sa.Integer, primary_key=True),
                   sa.Column('name', sa.String(255), nullable=False, unique=True)
                   )


user_company = sa.Table('user_company', metadata,
                        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.user_id'), primary_key=True,),
                        sa.Column('company_id', sa.Integer, sa.ForeignKey('company.company_id'), primary_key=True)
                        )


entry_category = sa.Table('entry_category', metadata,
                          sa.Column('category_id', sa.Integer, primary_key=True),
                          sa.Column('name', sa.String(255), nullable=False),
                          sa.Column('description', sa.String(255), nullable=True)
                          )


entry = sa.Table('entry', metadata,
                 sa.Column('entry_id', sa.Integer, primary_key=True),
                 sa.Column('amount', sa.Integer, nullable=False),
                 sa.Column('description', sa.String(255), nullable=False),
                 sa.Column('start_date', sa.Date, nullable=False),
                 sa.Column('occurring', sa.Integer, nullable=False),
                 sa.Column('days_between', sa.Integer, nullable=True),
                 sa.Column('category_id', sa.Integer, sa.ForeignKey('entry_category.category_id'), nullable=False),
                 sa.Column('company_id', sa.Integer, sa.ForeignKey('company.company_id'), nullable=False)
                 )