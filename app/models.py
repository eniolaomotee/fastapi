from .database import Base
from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# When it comes to building out our DB SQLalchemy has a limitiation, which doesn't allow us to modify columns and add foreign key constraints etc, once it sees the table it doesn't accept the new table changes so you'd have to drop the table and then it would load again


# So in order to achieve this, we'd have to use a tool know as Alembic which is a database migration tool.It's able to allow us to create incremental changes to our database and track it as well as well as roll the changes back at any point in time, we'd use a tool called alembic to make changes to our database


# Database migrations 

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content= Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # When setting up our FK, we pass in the tablename and the column we are referencing which is users.id and the ondelete method as well.
    owner_id  = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    # This returns the class of another model
    # Note we're not referencing the model but the actual class which is User
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # phone_number = Column(String)
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)



# Relationships in database : How you set up relationship within tables, setting relationships within 2 tables.
# 3 types of relationships a. One to one b. One to Many c. Many to Many.
# In our case we just need to create the user_id on the post table since it's a one to many relationship and that's the FK that's been mapped, also we want to make sure that the data type matches that of the key we're matching on the Users table as well.

# Set the relationship on the post table and map the contraints as well as the FK.




# SQL JOINS
# So we have different types of joins we have inner, outer,self,left etc.
# so let's say we have 2 tables basket_a and basket_b that do store fruits right, baseket A has fruit A column (1. Apple,2.Orange,3.Banana,4.Cucumber) and baseket B has fruit B column (1. Orange, 2. Apple,3. Watermelon,4.Pear), the tables do have some common fruits such as apple and orange right.

# SQL inner join: This joins the first table, basket_a with the second table, basket_b by matching the values in the fruit_a and fruit_b columns, so a sample output would be 1. Apple 2. Apple, 2. Orange 1.Orange that would be 2 rows

# SQL left join: This helps us to join the basket_a table with the basket_b tables. In this context, the first table, basket_a is the left table and the second table is called the right table, so a sample query for this would be:     1. Apple 2. Apple, 2. Orange 1.Orange, 3. Banana null, 4. Cucumber null so that would be a total of 4 rows.

# SQL left Outer Join: To select rows from the left table that do not have matching rows in the right table, you use the left join with a WHERE clause.     e.g select a,fruit_a, b, fruit_b from basket_a left join basket_b on fruit_a = fruit_b where b is null; Left join is the same as left outer join.

# SQL right join: just like left just that you're selecting data from the right table. In this context, the second table, basket_b is the right table and basket_ a is the left, so a sample query would be like this: 1.Orange 2. Orange, 2. Apple 1. Apple, 3. Watermelon null null, 4. Pear null null                          


# SQL full outer Join: it returns a set that contains all rows from left and right tables, with the matching rows from both sides if available. In case there is no match, the columns of the table will be filled with NULL. a sample query would be ,1. Apple 2. Apple, 2. Orange 1. Orange, 3.Banana null null,4. Cucumber null null, null null 3. Watermelon, null null 4.Pear. 

# 