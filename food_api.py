import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_nutrient.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
# Declare Food as a global variable
Food = None

def create_dynamic_model(name, columns, first_row_values):
    attrs = {'__tablename__': name.lower(), 'id': Column(Integer, primary_key=True)}

    # Define the serialize method within create_dynamic_model
    def serialize(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # Add the serialize method to the attrs dictionary
    attrs['serialize'] = serialize

    for col, first_val in zip(columns, first_row_values):
        try:
            # Attempt to determine if the column should be Float based on the first value
            float(first_val) if first_val != np.nan else np.nan
            attrs[col] = Column(Float)
        except (ValueError, TypeError):
            attrs[col] = Column(String)
    
    return type(name, (db.Model,), attrs)
# def create_dynamic_model(name, columns, first_row_values):
#     attrs = {'__tablename__': name.lower(), 'id': Column(Integer, primary_key=True)}
#     for col, first_val in zip(columns, first_row_values):
#         # Attempt to determine the data type based on the first value
#         try:
#             # Try converting the first value to a float
#             float(first_val)
#             # If successful, use Float type for the column
#             attrs[col] = Column(Float)
#         except (ValueError, TypeError):
#             # If conversion fails or the value is None, default to String type
#             attrs[col] = Column(String)
    
#     return type(name, (db.Model,), attrs)

def initialize_database():
    global Food  # Declare Food as global to modify it

    # Load the Excel file
    df = pd.read_excel('./Food_Nutrient_DB.xlsx')
    df.replace('1g 미만', np.nan, inplace=True)
    # Dynamically Create the Model with using df columns name   
    Food = create_dynamic_model('Food', df.columns,df.values[0])
    with app.app_context():
        db.create_all()
                # Filter or transform the DataFrame as necessary to match the database schema
        # For simplicity, assuming the DataFrame columns directly match the model's columns
        # Convert DataFrame to list of dictionaries
        food_data = df.to_dict(orient='records')

        # Insert data into the database
        for food_dict in food_data:
            food = Food(**food_dict)  # Assuming direct mapping for simplicity
            db.session.add(food)
        db.session.commit()

    # if not os.path.exists('food_nutrient.db'):
    #     db.create_all()



    #     # Filter or transform the DataFrame as necessary to match the database schema
    #     # For simplicity, assuming the DataFrame columns directly match the model's columns
    #     # Convert DataFrame to list of dictionaries
    #     food_data = df.to_dict(orient='records')

    #     # Insert data into the database
    #     for food_dict in food_data:
    #         food = Food(**food_dict)  # Assuming direct mapping for simplicity
    #         db.session.add(food)
    #     db.session.commit()
    # else:
    #     # If the DB exists, define Food based on the existing schema
    #     # This assumes the DB schema matches the Excel file used initially
    #     df = pd.read_excel('/mnt/data/Food_Nutrient_DB.xlsx')
    #     Food = create_dynamic_model('Food', df.columns.tolist())


initialize_database()
# @app.before_first_request
# def before_first_request():

@app.route('/foods/<int:id>', methods=['PUT'])
def update_food(id):
    food = Food.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(food, key, value)
    db.session.commit()
    return jsonify({'message': 'Food updated successfully.'})

@app.route('/foods/<int:id>', methods=['DELETE'])
def delete_food(id):
    food = Food.query.get_or_404(id)
    db.session.delete(food)
    db.session.commit()
    return jsonify({'message': 'Food deleted successfully.'})    

@app.route('/foods', methods=['GET'])
@app.route('/foods/<int:id>', methods=['GET'])
def read_foods(id=None):
    if id is None:
        foods = Food.query.all()
        return jsonify([food.serialize() for food in foods])
    else:
        food = Food.query.get_or_404(id)
        return jsonify(food.serialize())
    
# Define your API endpoints here

if __name__ == '__main__':
    app.run(debug=True)
