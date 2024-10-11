from flask import Blueprint, request, jsonify
from dbconnect import connection
import pyodbc

image_bp = Blueprint('image_bp', __name__)

# API to upload an image
@image_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        conn = connection()
        cursor = conn.cursor()

        # Get data from request
        data = request.get_json()
        user_id = data.get('user_id')
        blob_url = data.get('blob_url')
        image_name = data.get('image_name', '')
        description = data.get('description', '')
        file_size = data.get('file_size', 0)
        content_type = data.get('content_type', '')

        # Insert image data into the database
        query = """
        INSERT INTO images (user_id, blob_url, upload_timestamp, image_name, description, file_size, content_type)
        VALUES (?, ?, GETDATE(), ?, ?, ?, ?)
        """
        cursor.execute(query, (user_id, blob_url, image_name, description, file_size, content_type))
        conn.commit()

        return jsonify({"message": "Image uploaded successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# API to retrieve images for a specific user
@image_bp.route('/images/<int:user_id>', methods=['GET'])
def get_images(user_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        # Query to get images for the user
        query = "SELECT * FROM images WHERE user_id = ? AND is_deleted = 0"
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        # Format result
        images = []
        for row in rows:
            image = {
                "image_id": row[0],
                "user_id": row[1],
                "blob_url": row[2],
                "upload_timestamp": row[3],
                "image_name": row[4],
                "description": row[5],
                "file_size": row[6],
                "content_type": row[7]
            }
            images.append(image)

        return jsonify(images), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# API to soft delete an image
@image_bp.route('/images/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        conn = connection()
        cursor = conn.cursor()

        # Update query to mark image as deleted
        query = "UPDATE images SET is_deleted = 1 WHERE image_id = ?"
        cursor.execute(query, (image_id,))
        conn.commit()

        return jsonify({"message": "Image deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
