from extensions import mysql
from flask import current_app

# ✅ Approved Properties Only
def get_approved_properties():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM properties WHERE approved = TRUE")
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error getting approved properties: {e}")
        return []

# ✅ All Properties (Admin View)
def get_all_properties():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM properties")
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error getting all properties: {e}")
        return []

# ✅ Pending Properties Only
def get_pending_properties():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM properties WHERE approved = FALSE")
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error getting pending properties: {e}")
        return []

# ✅ Approve Property
def approve_property(property_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE properties SET approved = TRUE WHERE id = %s", (property_id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error approving property: {e}")

# ✅ Delete Property (Any)
def delete_property(property_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM properties WHERE id = %s", (property_id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error deleting property: {e}")

# ✅ Submit as Pending (Viewer)
def submit_pending_property(data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO properties (title, location, price, type, description, image_url, submitted_by, approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
        """, (
            data['title'], data['location'], data['price'],
            data['type'], data['description'], data['image_url'], data['submitted_by']
        ))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error submitting pending property: {e}")

# ✅ Add Property Directly (Admin)
def add_property(data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO properties (title, location, price, type, description, image_url, submitted_by, approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        """, (
            data['title'], data['location'], data['price'],
            data['type'], data['description'], data['image_url'], data['submitted_by']
        ))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error adding property directly: {e}")

# ✅ All Users (Admin)
def get_all_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error getting users: {e}")
        return []

# ✅ Add New User
def add_new_user(username, password, role):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, role))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error adding user: {e}")

# ✅ Delete User by ID
def delete_user_by_id(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error deleting user: {e}")

def get_all_pending_properties():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties WHERE approved = FALSE")
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    result = [dict(zip(columns, row)) for row in rows]
    cur.close()
    return result
    
# ✅ Get Property by ID
def get_property_by_id(property_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM properties WHERE id = %s", (property_id,))
        row = cur.fetchone()
        columns = [col[0] for col in cur.description]
        result = dict(zip(columns, row)) if row else None
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error getting property by id: {e}")
        return None

# ✅ Filtered & Sorted Properties
def get_filtered_properties(filters):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM properties WHERE approved = TRUE"
        params = []

        # Filtering
        if filters['location']:
            query += " AND location LIKE %s"
            params.append(f"%{filters['location']}%")
        if filters['min_price']:
            query += " AND price >= %s"
            params.append(filters['min_price'])
        if filters['max_price']:
            query += " AND price <= %s"
            params.append(filters['max_price'])
        if filters['type']:
            query += " AND type LIKE %s"
            params.append(f"%{filters['type']}%")

        # Sorting
        sort_option = filters['sort']
        if sort_option == "low_high":
            query += " ORDER BY price ASC"
        elif sort_option == "high_low":
            query += " ORDER BY price DESC"
        elif sort_option == "oldest":
            query += " ORDER BY id ASC"
        else:  # newest
            query += " ORDER BY id DESC"

        cur.execute(query, tuple(params))
        columns = [col[0] for col in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return result
    except Exception as e:
        current_app.logger.error(f"Error filtering properties: {e}")
        return []
